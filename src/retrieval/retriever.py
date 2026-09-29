import json
from pathlib import Path

from src.embeddings.embedder import Embedder
from src.vectorstore.faiss_store import (
    FAISSStore,
    load_metadata,
)


class Retriever:
    def __init__(
        self,
        index_path: str = "indexes/faiss/index.faiss",
        metadata_path: str = "indexes/faiss/metadata.json",
        children_path: str = "data/processed/children.json",
        parents_path: str = "data/processed/parents.json",
    ):
        self.embedder = Embedder()

        self.store = FAISSStore.load(index_path)

        self.metadata = load_metadata(metadata_path)

        self.children = self._load_json(children_path)
        self.parents = self._load_json(parents_path)

        self.children_by_id = {
            child["child_id"]: child
            for child in self.children
        }

        self.parents_by_id = {
            parent["parent_id"]: parent
            for parent in self.parents
        }

    @staticmethod
    def _load_json(path: str) -> list[dict]:
        with Path(path).open(
            encoding="utf-8"
        ) as file:
            return json.load(file)

    def search(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[dict]:

        # 1. Convert query into an embedding
        query_vector = self.embedder.embed_text(query)

        # 2. Search FAISS
        scores, indices = self.store.search(
            query_vector,
            top_k=top_k,
        )

        results = []

        # 3. Resolve FAISS index → metadata
        for rank, (score, index) in enumerate(
            zip(scores, indices),
            start=1,
        ):
            if index < 0:
                continue

            metadata = self.metadata[index]

            child_id = metadata["child_id"]
            parent_id = metadata["parent_id"]

            child = self.children_by_id[child_id]

            results.append(
                {
                    "rank": rank,
                    "score": score,
                    "faiss_index": index,
                    "child_id": child_id,
                    "parent_id": parent_id,
                    "title": child["title"],
                    "content": child["content"],
                }
            )

        return results

    def get_parents(
        self,
        results: list[dict],
    ) -> list[dict]:

        parents = []
        seen_parent_ids = set()

        for result in results:
            parent_id = result["parent_id"]

            if parent_id in seen_parent_ids:
                continue

            parent = self.parents_by_id[parent_id]

            parents.append(parent)
            seen_parent_ids.add(parent_id)

        return parents