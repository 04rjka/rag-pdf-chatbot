from fastapi import APIRouter,UploadFile,File,Depends
from app.models.user import User
from app.dependencies import get_current_user,get_document_service
from app.services.document_service import DocumentService

router = APIRouter(prefix="/documents",tags=["Documents"])

@router.post("/upload")
async def upload_document(file:UploadFile = File(...),document_service:DocumentService=Depends(get_document_service),current_user : User = Depends(get_current_user)):
    result = await document_service.upload(file,current_user=current_user)
    return result

@router.get("")
def get_documents(current_user:User = Depends(get_current_user),document_service:DocumentService=Depends(get_document_service)):
    return document_service.get_user_documents(user_id=current_user.id)