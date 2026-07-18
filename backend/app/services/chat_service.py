from app.rag.retriever import retrieve
from app.rag.chains import rag_chain

question = "what is a database ?"

docs = retrieve(question)

context="\n\n".join(
    doc.page_content
    for doc in docs
)

response = rag_chain.invoke({
    "context":context,
    "question":question
})

print(response.content)