from fastapi import FastAPI
from app.rag.retriever import retrieve
from app.rag.chains import rag_chain

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