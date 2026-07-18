from app.rag.prompts import prompt
from app.rag.llm import llm

rag_chain = prompt | llm