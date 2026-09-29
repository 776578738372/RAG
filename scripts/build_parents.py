import json
from pathlib import Path

from src.ingestion.loader import load_pdf
from src.ingestion.structure import build_structure_blocks
from src.ingestion.models import ParentDocument


PDF_PATH = Path("data/raw/hawkvision_product_spec.pdf")

OUTPUT_PATH = Path(
    "data/processed/parents.json"
)

DOCUMENT_ID = "hawkvision_product_spec"


def build_parents():

    pages = load_pdf(str(PDF_PATH))

    blocks = build_structure_blocks(pages)

    parents = []

    parent_counter = 0

    for block in blocks:

        # ---------------------------------------------
        # Section 5 is evaluation data.
        # Do NOT index it as knowledge.
        # ---------------------------------------------

        if block.section_number == "5":
            continue

        parent_id = f"parent_{parent_counter:05d}"

        parent = ParentDocument(
            parent_id=parent_id,
            document_id=DOCUMENT_ID,

            section_number=block.section_number,
            section_title=block.section_title,

            subsection_number=block.subsection_number,
            title=block.title,

            page_start=block.page_start,
            page_end=block.page_end,

            content=block.content,
        )

        parents.append(parent)

        parent_counter += 1

    return parents


def serialize_parent(parent: ParentDocument) -> dict:

    return {
        "parent_id": parent.parent_id,
        "document_id": parent.document_id,

        "section_number": parent.section_number,
        "section_title": parent.section_title,

        "subsection_number": parent.subsection_number,
        "title": parent.title,

        "page_start": parent.page_start,
        "page_end": parent.page_end,

        "content": parent.content,

        "children": parent.children,
    }


def main():

    parents = build_parents()

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    data = [
        serialize_parent(parent)
        for parent in parents
    ]

    with OUTPUT_PATH.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            data,
            file,
            indent=2,
            ensure_ascii=False,
        )

    print(
        f"Created {len(parents)} parent documents"
    )

    print(
        f"Saved to: {OUTPUT_PATH}"
    )

    print()

    for parent in parents:

        print(
            f"{parent.parent_id} | "
            f"Section {parent.section_number} | "
            f"{parent.title} | "
            f"Pages {parent.page_start}-{parent.page_end}"
        )


if __name__ == "__main__":
    main()