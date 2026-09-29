import json
from pathlib import Path

from src.embeddings.embedder import Embedder
from src.vectorstore.faiss_store import FAISSStore, save_metadata


CHILDREN_PATH = Path("data/processed/children.json")

INDEX_PATH = Path("indexes/faiss/index.faiss")
METADATA_PATH = Path("indexes/faiss/metadata.json")


def load_children() -> list[dict]:
    with CHILDREN_PATH.open(
        encoding="utf-8"
    ) as file:
        return json.load(file)


def main():
    children = load_children()

    print(f"Loaded {len(children)} child chunks")

    texts = [
        child["content"]
        for child in children
    ]

    print("Loading embedding model...")

    embedder = Embedder()

    print("Creating embeddings...")

    vectors = embedder.embed_documents(texts)

    dimension = len(vectors[0])

    print(f"Embedding dimension: {dimension}")
    print(f"Generated vectors: {len(vectors)}")

    store = FAISSStore(
        dimension=dimension
    )

    store.add(vectors)

    metadata = []

    for faiss_index, child in enumerate(children):
        metadata.append(
            {
                "faiss_index": faiss_index,
                "child_id": child["child_id"],
                "parent_id": child["parent_id"],
            }
        )

    store.save(INDEX_PATH)
    save_metadata(
        metadata,
        METADATA_PATH,
    )

    print()
    print("FAISS index built successfully")
    print(f"Vectors in index: {len(store)}")
    print(f"Index saved to: {INDEX_PATH}")
    print(f"Metadata saved to: {METADATA_PATH}")


if __name__ == "__main__":
    main()