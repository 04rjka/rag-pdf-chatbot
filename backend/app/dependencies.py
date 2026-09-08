from functools import lru_cache
from fastapi import Depends
from sqlalchemy.orm import Session

from app.config import settings
from app.db.db import get_db

from app.rag.embeddings import EmbeddingService
from app.rag.vector_store import VectorStore
from app.rag.retriever import Retriever
from app.rag.chains import rag_chain,query_formulation_chain
from app.rag.chunking import DocumentSplitter
from app.rag.pdf_loader import PDFLoader

from app.services.chat_service import ChatService
from app.services.ingestion_service import IngestionService
from app.services.document_service import DocumentService

from app.auth.dependencies import get_current_user

# embedding = EmbeddingService()

# vector_store = VectorStore(db_path=settings.chroma_path,embedding=embedding.get())

# chroma = vector_store.load()

# retriever = Retriever(vectorstore=chroma,k = 5)

# chat_service = ChatService(retriever=retriever,rag_chain=rag_chain)

# ingestion_service = IngestionService(pdf_loader=PDFLoader(),splitter=DocumentSplitter(),vector_store=vector_store)

# document_service = DocumentService(ingestion_service=ingestion_service)

@lru_cache
def get_embedding_service():
    return EmbeddingService()

@lru_cache
def get_vector_store(embedding_service: EmbeddingService = Depends(get_embedding_service)):
    return VectorStore(db_path=settings.chroma_path,embedding=embedding_service.get())

@lru_cache
def get_pdf_loader() -> PDFLoader:
    return PDFLoader()

@lru_cache
def get_document_splitter() -> DocumentSplitter:
    return DocumentSplitter()

def get_retriever(vector_store:VectorStore=Depends(get_vector_store)):
    return Retriever(vectorstore=vector_store.db,k=5)

def get_ingestion_service(pdf_loader:PDFLoader = Depends(get_pdf_loader),splitter:DocumentSplitter= Depends(get_document_splitter),vector_store:VectorStore= Depends(get_vector_store)):
    return IngestionService(pdf_loader=pdf_loader,splitter=splitter,vector_store=vector_store)

def get_document_service(db:Session=Depends(get_db),ingestion_service:IngestionService=Depends(get_ingestion_service)):
    return DocumentService(db=db,ingestion_service=ingestion_service)

def get_chat_service(retriever:Retriever=Depends(get_retriever),db:Session=Depends(get_db)):
    return ChatService(retriever=retriever,rag_chain=rag_chain,query_formulation_chain=query_formulation_chain,db=db)