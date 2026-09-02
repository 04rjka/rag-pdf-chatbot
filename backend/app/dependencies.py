from app.rag.embeddings import EmbeddingService
from app.rag.vector_store import VectorStore
from app.rag.retriever import Retriever
from app.rag.chains import rag_chain
from app.services.chat_service import ChatService

DB_PATH = "./backend/storage/chroma"

embedding = EmbeddingService()

vector_store = VectorStore(db_path=DB_PATH,embedding=embedding.get())

chroma = vector_store.load()

retriever = Retriever(vectorstore=chroma,k = 5)

chat_service = ChatService(retriever=retriever,rag_chain=rag_chain)