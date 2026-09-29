from fastapi import APIRouter
from pydantic import BaseModel

from src.pipeline.rag import RAG


router = APIRouter()

rag = RAG(top_k=5)


class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    question: str
    answer: str


@router.post("/query", response_model=QueryResponse)
def query_rag(request: QueryRequest):
    result = rag.ask(request.question)

    return QueryResponse(
        question=request.question,
        answer=result["answer"],
    )