import json
from pathlib import Path

import faiss
import numpy as np


class FAISSStore:
    def __init__(self, dimension: int):
        self.dimension = dimension

        # Inner Product because our embeddings are normalized.
        # For normalized vectors:
        # Inner Product == Cosine Similarity
        self.index = faiss.IndexFlatIP(dimension)

    def add(self, vectors: list[list[float]]) -> None:
        matrix = np.asarray(vectors, dtype="float32")

        if matrix.ndim != 2:
            raise ValueError("vectors must be a 2D list")

        if matrix.shape[1] != self.dimension:
            raise ValueError(
                f"Expected dimension {self.dimension}, "
                f"got {matrix.shape[1]}"
            )

        self.index.add(matrix)

    def search(
        self,
        query_vector: list[float],
        top_k: int = 5,
    ) -> tuple[list[float], list[int]]:
        query = np.asarray(
            [query_vector],
            dtype="float32",
        )

        scores, indices = self.index.search(
            query,
            top_k,
        )

        return scores[0].tolist(), indices[0].tolist()

    def save(self, path: str | Path) -> None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        faiss.write_index(
            self.index,
            str(path),
        )

    @classmethod
    def load(cls, path: str | Path):
        index = faiss.read_index(str(path))

        store = cls(index.d)
        store.index = index

        return store

    def __len__(self) -> int:
        return self.index.ntotal


def save_metadata(
    metadata: list[dict],
    path: str | Path,
) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        json.dump(
            metadata,
            file,
            indent=2,
            ensure_ascii=False,
        )


def load_metadata(path: str | Path) -> list[dict]:
    with Path(path).open(
        encoding="utf-8"
    ) as file:
        return json.load(file)