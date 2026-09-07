from fastapi import APIRouter,UploadFile,File
from app.dependencies import document_service

router = APIRouter(prefix="/documents",tags=["Documents"])

@router.post("/upload")
async def upload_document(file:UploadFile = File(...)):
    result = await document_service.upload(file)
    return result