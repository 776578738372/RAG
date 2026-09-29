from dataclasses import dataclass
import re

from src.ingestion.loader import Page
from src.ingestion.semantic_headings import get_semantic_heading


SECTION_PATTERN = re.compile(
    r"^Section\s+(\d+)\s*[\ue092:\-]\s*(.+)$",
    re.IGNORECASE,
)

SUBSECTION_PATTERN = re.compile(
    r"^(\d+\.\d+)\s+(.+)$"
)


@dataclass
class StructureBlock:
    section_number: str
    section_title: str
    subsection_number: str | None
    title: str
    page_start: int
    page_end: int
    content: str


def detect_section_heading(line: str):
    match = SECTION_PATTERN.match(line.strip())

    if not match:
        return None

    return {
        "section_number": match.group(1),
        "title": match.group(2).strip(),
    }


def detect_subsection_heading(line: str):
    match = SUBSECTION_PATTERN.match(line.strip())

    if not match:
        return None

    return {
        "subsection_number": match.group(1),
        "title": match.group(2).strip(),
    }


def build_structure_blocks(
    pages: list[Page],
) -> list[StructureBlock]:

    blocks = []

    current_section_number = None
    current_section_title = None
    current_subsection_number = None
    current_title = None
    current_page_start = None
    current_content = []

    def flush(page_number: int):
        nonlocal current_content

        if not current_title:
            return

        content = "\n".join(current_content).strip()

        if not content:
            current_content = []
            return

        blocks.append(
            StructureBlock(
                section_number=current_section_number,
                section_title=current_section_title,
                subsection_number=current_subsection_number,
                title=current_title,
                page_start=current_page_start,
                page_end=page_number,
                content=content,
            )
        )

        current_content = []

    for page in pages:

        for raw_line in page.text.splitlines():

            line = raw_line.strip()

            if not line:
                continue

            # --------------------------------------------------
            # Section heading
            # --------------------------------------------------

            section = detect_section_heading(line)

            if section:

                flush(page.page_number)

                current_section_number = section["section_number"]
                current_section_title = section["title"]

                current_subsection_number = None

                # Section 1 gets a semantic overview parent.
                # Section 2 gets an architecture overview parent.
                if current_section_number == "1":
                    current_title = "Section 1 Overview"

                elif current_section_number == "2":
                    current_title = "Architecture Overview"

                else:
                    current_title = current_section_title

                current_page_start = page.page_number

                continue

            # --------------------------------------------------
            # Numbered subsection
            # Example:
            # 3.1 Home Tab
            # 4.1 Complete Sample JSON...
            # --------------------------------------------------

            subsection = detect_subsection_heading(line)

            if subsection:

                flush(page.page_number)

                current_subsection_number = (
                    subsection["subsection_number"]
                )

                current_title = subsection["title"]

                current_page_start = page.page_number

                continue

            # --------------------------------------------------
            # Semantic heading
            # Sections 1 and 2
            # --------------------------------------------------

            semantic_heading = get_semantic_heading(
                current_section_number,
                line,
            )

            if semantic_heading:

                flush(page.page_number)

                current_subsection_number = None

                current_title = semantic_heading

                current_page_start = page.page_number

                continue

            # --------------------------------------------------
            # Normal content
            # --------------------------------------------------

            if current_title:
                current_content.append(line)

    # Flush final block
    if pages:
        flush(pages[-1].page_number)

    return blocks