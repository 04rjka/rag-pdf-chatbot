from app.rag.vector_store import load_db

db = load_db()

retriever = db.as_retriever(
    search_kwargs={
        "k":5
    }
)

def retrieve(question):
    return retriever.invoke(question)

class Retriever:
    def __init__(self, vectorstore, k: int = 5):
        self.vectorstore = vectorstore
        self.k = k

    def retrieve(self, question):
        retriever = self.vectorstore.as_retriever(
            search_kwargs={
                "k":self.k
            }
        )
        return retriever.invoke(question)