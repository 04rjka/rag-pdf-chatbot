from app.rag.retriever import retrieve,Retriever
from app.rag.chains import rag_chain
from app.rag.embeddings import EmbeddingService
from app.rag.vector_store import VectorStore

question = "what is a database ?"

docs = retrieve(question)

context="\n\n".join(
    doc.page_content
    for doc in docs
)

response = rag_chain.invoke({
    "context":context,
    "question":question
})

print(response.content)

class ChatService:
    def __init__(self,retriever,rag_chain):
        self.retriever = retriever
        self.rag_chain = rag_chain

    def ask(self,question):
        docs = self.retriever.retrieve(question)

        context="\n\n".join(
            doc.page_content
            for doc in docs
            )
        return self.rag_chain.invoke({
            "context":context,
            "question":question
        })