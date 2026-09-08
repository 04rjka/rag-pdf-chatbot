from app.rag.prompts import prompt,contextualize_q_prompt,qa_prompt
from app.rag.llm import llm
from langchain_core.output_parsers import StrOutputParser

rag_chain = qa_prompt | llm | StrOutputParser()

query_formulation_chain = contextualize_q_prompt | llm | StrOutputParser()