from app.rag.vector_store import load_db

db = load_db()

retriever = db.as_retriever(
    search_kwargs={
        "k":5
    }
)

def retrieve(question):
    return retriever.invoke(question)