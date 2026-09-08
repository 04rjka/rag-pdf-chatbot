from fastapi import APIRouter,Depends,status
from app.dependencies import get_chat_service,get_current_user
from app.models.user import User
from app.services.chat_service import ChatService
from typing import Optional
from app.schemas.chat import ChatRequest

router = APIRouter(prefix="/chat",tags=["Chat"])

@router.post("",status_code=status.HTTP_200_OK)
def chat(payload:ChatRequest,chat_service:ChatService=Depends(get_chat_service),current_user:User=Depends(get_current_user)):
    response = chat_service.ask(question=payload.question,document_id=payload.document_id,user_id=current_user.id)
    return response