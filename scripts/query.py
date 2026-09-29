from src.pipeline.rag import RAG


def main():
    rag = RAG(top_k=5)

    question = "Name the five primary safety and operational usecases supported by HawkVision AI"
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