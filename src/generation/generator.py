import os

from dotenv import load_dotenv
from openai import OpenAI

from src.generation.prompt import SYSTEM_PROMPT

load_dotenv()


class Generator:
    def __init__(
        self,
        model: str = "gpt-5.6-luna",
    ):
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY is not set"
            )

        self.client = OpenAI(
            api_key=api_key
        )

        self.model = model

    def generate(
        self,
        prompt: str,
    ) -> str:

        response = self.client.responses.create(
            model=self.model,
            instructions=SYSTEM_PROMPT,
            input=prompt,
        )

        return response.output_text