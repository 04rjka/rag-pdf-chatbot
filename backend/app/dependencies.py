from app.config import settings
from app.rag.embeddings import EmbeddingService
from app.rag.vector_store import VectorStore
from app.rag.retriever import Retriever
from app.rag.chains import rag_chain
from app.rag.chunking import DocumentSplitter
from app.rag.pdf_loader import PDFLoader
from app.services.chat_service import ChatService
from app.services.ingestion_service import IngestionService
from app.services.document_service import DocumentService

embedding = EmbeddingService()

vector_store = VectorStore(db_path=settings.chroma_path,embedding=embedding.get())

chroma = vector_store.load()

retriever = Retriever(vectorstore=chroma,k = 5)

chat_service = ChatService(retriever=retriever,rag_chain=rag_chain)

ingestion_service = IngestionService(pdf_loader=PDFLoader(),splitter=DocumentSplitter(),vector_store=vector_store)

document_service = DocumentService(ingestion_service=ingestion_service)