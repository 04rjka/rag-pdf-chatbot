from langchain_chroma import Chroma

class VectorStore:
    def __init__(self, db_path, embedding):
        self.db_path = db_path
        self.embedding = embedding
        self.db = Chroma(persist_directory=self.db_path,embedding_function=self.embedding)

    def add(self,chunks):
        return self.db.add_documents(chunks) 
    
    def load(self):
        return self.db