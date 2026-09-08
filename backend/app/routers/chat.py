from fastapi import APIRouter,Depends
from app.dependencies import get_chat_service,get_current_user
from app.models.user import User
from app.services.chat_service import ChatService
from typing import Optional

router = APIRouter(prefix="/chat",tags=["Chat"])

@router.get("/{question}")
def chat(question: str,conversation_id:Optional[int]=None,chat_service:ChatService=Depends(get_chat_service),current_user:User=Depends(get_current_user)):
    response = chat_service.ask(question=question,user_id=current_user.id)
    return response