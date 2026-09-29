SYSTEM_PROMPT = """You are a helpful assistant for the HawkVision AI
product knowledge base.

Answer the user's question using only the provided context.

Rules:
- Do not invent information that is not present in the context.
- If the context does not contain enough information, say so clearly.
- Give a concise and accurate answer.
- Preserve HawkVision's terminology.
"""


def build_prompt(
    question: str,
    contexts: list[dict],
) -> str:
    context_parts = []

    for index, context in enumerate(contexts, start=1):
        context_parts.append(
            f"""Context {index}
Title: {context["title"]}
Section: {context["section_number"]}
Pages: {context["page_start"]}-{context["page_end"]}

{context["content"]}
"""
        )

    context_text = "\n\n".join(context_parts)

    return f"""Context:

{context_text}

User Question:
{question}
"""