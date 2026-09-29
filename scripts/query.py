from src.pipeline.rag import RAG


def main():
    rag = RAG(top_k=5)

    question = "What are the three core structural tiers of the HawkVision AI organizational hierarchy, and what key configuration entities are defined at Tier 2?"

    result = rag.ask(question)

    print("=" * 80)
    print("QUESTION")
    print("=" * 80)
    print(question)

    print()
    print("=" * 80)
    print("ANSWER")
    print("=" * 80)
    print(result["answer"])

    print()
    print("=" * 80)
    print("RETRIEVED PARENTS")
    print("=" * 80)

    for parent in result["parent_results"]:
        print(
            f"{parent['parent_id']} | "
            f"{parent['title']}"
        )


if __name__ == "__main__":
    main()