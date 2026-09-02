from fastapi import FastAPI
from app.dependencies import chat_service

app = FastAPI()

@app.get("/")
def health():
    return "Server Active"

@app.get("/chat/{question}")
def chat(question: str):
    response = chat_service.ask(question=question)
    return response.content