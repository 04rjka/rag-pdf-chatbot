from typing import Optional
class Retriever:
    def __init__(self, vectorstore, k: int = 5):
        self.vectorstore = vectorstore
        self.k = k

    def retrieve(self, question,user_id:int,document_id:Optional[int]):

        if document_id:
            where_filter = {"user_id":user_id}
        else:
            where_filter = {
                "$and":[
                    {"user_id":user_id},
                    {"document_id":document_id}
                ]
            }

        retriever = self.vectorstore.as_retriever(
            search_kwargs={
                "k":self.k,
                "filter": where_filter
            }
        )
        return retriever.invoke(question)