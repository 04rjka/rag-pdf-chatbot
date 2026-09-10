from fastapi import APIRouter,Depends,status
from fastapi.responses import StreamingResponse
from app.dependencies import get_chat_service,get_current_user
from app.models.user import User
from app.services.chat_service import ChatService
from typing import Optional
from app.schemas.chat import ChatRequest

router = APIRouter(prefix="/chat",tags=["Chat"])

@router.post("",status_code=status.HTTP_200_OK)
async def chat(payload:ChatRequest,chat_service:ChatService=Depends(get_chat_service),current_user:User=Depends(get_current_user)):
    generator = chat_service.ask(question=payload.question,document_id=payload.document_id,conversation_id=payload.conversation_id,user_id=current_user.id)
    return StreamingResponse(generator,media_type="text/event-stream",headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        })

@router.get("/conversations")
def get_conversations(current_user:User = Depends(get_current_user),chat_service:ChatService= Depends(get_chat_service)):
    return chat_service.get_conversations(user_id=current_user.id)

@router.get("/conversations/{conversation_id}/messages")
def get_conversations(conversation_id:int,current_user:User = Depends(get_current_user),chat_service:ChatService= Depends(get_chat_service)):
    return chat_service.get_conversation_messages(user_id=current_user.id,conversation_id=conversation_id)