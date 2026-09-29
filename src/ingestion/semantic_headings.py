import re


SECTION_1_HEADINGS = {
    "Supported Safety Usecases",
    "Core Design Principles",
}


SECTION_2_HEADINGS = {
    "Tier 1: Customer",
    "Tier 2: Site",
    "Tier 3: Camera",
    "Functional Tag Mechanism",
}


def normalize_heading(line: str) -> str:
    """
    Normalize PDF-specific Unicode characters.
    """

    return (
        line
        .replace("\ue092", ":")
        .replace("\ue081", "(")
        .replace("\ue082", ")")
        .replace("\ue088", "(")
        .replace("\ue098", ")")
        .strip()
    )


def clean_diagram_line(line: str) -> str:
    """
    Remove box-drawing characters and surrounding whitespace.
    """

    line = normalize_heading(line)

    # Remove common box-drawing characters
    line = re.sub(r"[│┃║┌┐└┘├┤┬┴┼─━═]", " ", line)

    # Collapse whitespace
    line = re.sub(r"\s+", " ", line)

    return line.strip()


def get_semantic_heading(
    section_number: str,
    line: str,
) -> str | None:

    # Do not treat diagram labels as structural headings.
    if any(char in line for char in "│┃║┌┐└┘├┤┬┴┼─━═"):
        return None

    normalized = clean_diagram_line(line)

    # -----------------------------------------
    # Section 1
    # -----------------------------------------

    if section_number == "1":

        if normalized in SECTION_1_HEADINGS:
            return normalized

    # -----------------------------------------
    # Section 2
    # -----------------------------------------

    if section_number == "2":

        if normalized in SECTION_2_HEADINGS:
            return normalized

        tier_match = re.fullmatch(
            r"Tier\s+(1|2|3)\s*:\s*"
            r"(Customer|Site|Camera)"
            r"(?:\s*\(.*\))?",
            normalized,
            re.IGNORECASE,
        )

        if tier_match:

            tier_number = tier_match.group(1)
            entity = tier_match.group(2).title()

            return f"Tier {tier_number}: {entity}"

    return None