from fastapi import APIRouter
from app.dependencies import chat_service

router = APIRouter(prefix="/chat",tags=["Chat"])

@router.get("/{question}")
def chat(question: str):
    response = chat_service.ask(question=question)
    return response.content