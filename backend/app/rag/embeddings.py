from langchain_huggingface import HuggingFaceEmbeddings

class EmbeddingService:
    def __init__(self):
        self.model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    def get(self):
        return self.model