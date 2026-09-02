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

class VectorStore:
    def __init__(self, db_path, embedding):
        self.db_path = db_path
        self.embedding = embedding

    def create_db(self,chunks):
        self.db = Chroma.from_documents(
            embedding=self.embedding,
            documents=chunks,
            persist_directory=self.db_path
            )
        return self.db
    def load(self):
        self.db = Chroma(
            persist_directory=self.db_path,
            embedding_function=self.embedding
            )
        return self.db