from langchain_google_genai import ChatGoogleGenerativeAI
from app.config import settings

llm = ChatGoogleGenerativeAI(
    model=settings.llm_model,
    google_api_key=settings.google_api_key
)