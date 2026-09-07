class Retriever:
    def __init__(self, vectorstore, k: int = 5):
        self.vectorstore = vectorstore
        self.k = k

    def retrieve(self, question,user_id:int):
        retriever = self.vectorstore.as_retriever(
            search_kwargs={
                "k":self.k,
                "filter":{"user_id":user_id}
            }
        )
        return retriever.invoke(question)