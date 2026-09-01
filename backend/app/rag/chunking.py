from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(chunk_size = 500,chunk_overlap=100)

def split_documents(documents):
    return splitter.split_documents(documents)

class DocumentSplitter:
    def __init__(self, chunk_size=500,chunk_overlap=100):
        self.splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size,chunk_overlap=chunk_overlap)

    def split_documents(self,documents):
        return self.splitter.split_documents(documents)