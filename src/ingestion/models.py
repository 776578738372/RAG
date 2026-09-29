from dataclasses import dataclass, field


@dataclass
class ParentDocument:
    parent_id: str

    document_id: str

    section_number: str
    section_title: str

    subsection_number: str | None
    title: str

    page_start: int
    page_end: int

    content: str

    children: list[str] = field(default_factory=list)

@dataclass
class ParentDocument:
    parent_id: str
    document_id: str

    section_number: str
    section_title: str

    subsection_number: str | None
    title: str

    page_start: int
    page_end: int

    content: str

    children: list[str] = field(default_factory=list)


def parent_from_dict(data: dict) -> ParentDocument:
    return ParentDocument(
        parent_id=data["parent_id"],
        document_id=data["document_id"],
        section_number=data["section_number"],
        section_title=data["section_title"],
        subsection_number=data["subsection_number"],
        title=data["title"],
        page_start=data["page_start"],
        page_end=data["page_end"],
        content=data["content"],
        children=data.get("children", []),
    )