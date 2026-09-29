import json
from pathlib import Path

from src.chunking.child_chunker import ChildChunker
from src.ingestion.models import parent_from_dict


PARENTS_PATH = Path(
    "data/processed/parents.json"
)

CHILDREN_PATH = Path(
    "data/processed/children.json"
)


def load_parents():

    with PARENTS_PATH.open(
        encoding="utf-8"
    ) as file:

        data = json.load(file)

    return [
        parent_from_dict(item)
        for item in data
    ]


def serialize_child(child):

    return {
        "child_id": child.child_id,
        "parent_id": child.parent_id,
        "document_id": child.document_id,

        "section_number": child.section_number,
        "section_title": child.section_title,

        "subsection_number": child.subsection_number,
        "title": child.title,

        "page_start": child.page_start,
        "page_end": child.page_end,

        "chunk_index": child.chunk_index,

        "content": child.content,

        "token_count": child.token_count,
    }


def main():

    parents = load_parents()

    print(f"Loaded {len(parents)} parents")

    chunker = ChildChunker(
        chunk_size=500,
        overlap=100,
    )

    children = chunker.chunk_parents(
        parents
    )

    serialized_children = [
        serialize_child(child)
        for child in children
    ]

    CHILDREN_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with CHILDREN_PATH.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            serialized_children,
            file,
            indent=2,
            ensure_ascii=False,
        )

    print(
        f"Created {len(children)} child chunks"
    )

    print(
        f"Saved to: {CHILDREN_PATH}"
    )


if __name__ == "__main__":
    main()