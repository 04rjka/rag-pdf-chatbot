from fastapi import FastAPI
from app.rag.retriever import retrieve
from app.rag.chains import rag_chain
from app.dependencies import chat_service

app = FastAPI()

@app.get("/")
def home():
    return "TEST"

@app.get("/ask/{question}")
def ask(question:str):
    docs = retrieve(question)

    context="\n\n".join(
    doc.page_content
    for doc in docs
    )
    response = rag_chain.invoke({
    "context":context,
    "question":question
    })

    return response.content

@app.get("/chat/{question}")
def chat(question: str):
    response = chat_service.ask(question=question)
    return response.content