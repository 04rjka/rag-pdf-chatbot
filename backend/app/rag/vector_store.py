from langchain_chroma import Chroma

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