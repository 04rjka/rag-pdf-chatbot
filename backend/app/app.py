from fastapi import FastAPI,UploadFile,File
from app.dependencies import chat_service,document_service,ingestion_service
from app.routers.auth import router as auth_router

app = FastAPI()

app.include_router(auth_router)

@app.get("/")
def health():
    return "Server Active"

@app.get("/chat/{question}")
def chat(question: str):
    response = chat_service.ask(question=question)
    return response.content

@app.post("/upload")
async def upload_document(file:UploadFile = File(...)):
    result = await document_service.upload(file)
    return result