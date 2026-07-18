from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template("""
Answer only using the provided context.

Context:
{context}

Question:
{question}
""")