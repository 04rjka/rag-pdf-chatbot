from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

DB_PATH = "./backend/storage/chroma"

def create_db(chunks):
    db = Chroma.from_documents(
        embedding=embedding,
        documents=chunks,
        persist_directory=DB_PATH
    )
    return db

def load_db():
    return Chroma(
        persist_directory=DB_PATH,
        embedding_function=embedding
    )