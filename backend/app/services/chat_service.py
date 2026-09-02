class ChatService:
    def __init__(self,retriever,rag_chain):
        self.retriever = retriever
        self.rag_chain = rag_chain

    def ask(self,question):
        docs = self.retriever.retrieve(question)

        context="\n\n".join(
            doc.page_content
            for doc in docs
            )
        return self.rag_chain.invoke({
            "context":context,
            "question":question
        })