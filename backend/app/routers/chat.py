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
    conversation = chat_service.get_or_create_conversation(conversation_id=payload.conversation_id,document_id=payload.document_id,user_id=current_user.id,initial_title=payload.question)
    generator = chat_service.ask(question=payload.question,user_id=current_user.id,conversation=conversation)
    return StreamingResponse(generator,media_type="text/event-stream",headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        })

@router.get("/conversations")
def get_conversations(current_user:User = Depends(get_current_user),chat_service:ChatService= Depends(get_chat_service)):
    return chat_service.get_conversations(user_id=current_user.id)

@router.get("/conversations/{conversation_id}")
def get_conversation(conversation_id: int, current_user: User = Depends(get_current_user),chat_service: ChatService = Depends(get_chat_service)):
    conv = chat_service.get_conversation(user_id=current_user.id, conversation_id=conversation_id)
    return {
        "id": conv.id,
        "title": conv.title,
        "document": {"id": conv.document.id, "filename": conv.document.filename} if conv.document else None,
    }

@router.get("/conversations/{conversation_id}/messages")
def get_conversation_messages(conversation_id:int,current_user:User = Depends(get_current_user),chat_service:ChatService= Depends(get_chat_service)):
    return chat_service.get_conversation_messages(user_id=current_user.id,conversation_id=conversation_id)

@router.delete("/conversations/{conversation_id}/delete",status_code=status.HTTP_204_NO_CONTENT)
def delete_conversation(conversation_id:int,current_user:User = Depends(get_current_user),chat_service:ChatService = Depends(get_chat_service)):
    chat_service.delete_conversation(user_id=current_user.id,conversation_id=conversation_id)