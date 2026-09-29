from dataclasses import dataclass

import tiktoken

from src.ingestion.models import ParentDocument


@dataclass
class ChildChunk:
    child_id: str
    parent_id: str
    document_id: str

    section_number: str
    section_title: str

    subsection_number: str | None
    title: str

    page_start: int
    page_end: int

    chunk_index: int
    content: str

    token_count: int


class ChildChunker:

    def __init__(
        self,
        chunk_size: int = 500,
        overlap: int = 100,
        encoding_name: str = "cl100k_base",
    ):
        if overlap >= chunk_size:
            raise ValueError(
                "overlap must be smaller than chunk_size"
            )

        self.chunk_size = chunk_size
        self.overlap = overlap

        self.encoding = tiktoken.get_encoding(
            encoding_name
        )

    def tokenize(self, text: str) -> list[int]:
        return self.encoding.encode(text)

    def detokenize(self, tokens: list[int]) -> str:
        return self.encoding.decode(tokens)

    def chunk_parent(
        self,
        parent: ParentDocument,
    ) -> list[ChildChunk]:

        tokens = self.tokenize(parent.content)

        if not tokens:
            return []

        chunks = []

        start = 0
        chunk_index = 0

        while start < len(tokens):

            end = min(
                start + self.chunk_size,
                len(tokens),
            )

            chunk_tokens = tokens[start:end]

            content = self.detokenize(
                chunk_tokens
            ).strip()

            child_id = (
                f"{parent.parent_id}"
                f"_child_{chunk_index:03d}"
            )

            chunks.append(
                ChildChunk(
                    child_id=child_id,

                    parent_id=parent.parent_id,

                    document_id=parent.document_id,

                    section_number=parent.section_number,

                    section_title=parent.section_title,

                    subsection_number=(
                        parent.subsection_number
                    ),

                    title=parent.title,

                    page_start=parent.page_start,

                    page_end=parent.page_end,

                    chunk_index=chunk_index,

                    content=content,

                    token_count=len(chunk_tokens),
                )
            )

            chunk_index += 1

            # Last chunk
            if end >= len(tokens):
                break

            start = end - self.overlap

        return chunks

    def chunk_parents(
        self,
        parents: list[ParentDocument],
    ) -> list[ChildChunk]:

        all_children = []

        for parent in parents:

            children = self.chunk_parent(parent)

            all_children.extend(children)

        return all_children