from src.generation.generator import Generator
from src.generation.prompt import build_prompt
from src.retrieval.retriever import Retriever


class RAG:
    def __init__(
        self,
        top_k: int = 5,
    ):
        self.retriever = Retriever()
        self.generator = Generator()

        self.top_k = top_k

    def ask(
        self,
        question: str,
    ) -> dict:

        # Retrieval
        child_results = self.retriever.search(
            question,
            top_k=self.top_k,
        )

        # Parent expansion
        parent_results = self.retriever.get_parents(
            child_results
        )

        # Prompt construction
        prompt = build_prompt(
            question,
            parent_results,
        )

        # Generation
        answer = self.generator.generate(
            prompt
        )

        return {
            "question": question,
            "answer": answer,
            "child_results": child_results,
            "parent_results": parent_results,
        }