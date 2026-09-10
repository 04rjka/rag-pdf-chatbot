from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from langchain_core.messages import AIMessage,HumanMessage
from fastapi import HTTPException,status
import json

from app.models.chat import Conversation, Message

class ChatService:
    def __init__(self,retriever,rag_chain,query_formulation_chain,db: Session):
        self.retriever = retriever
        self.rag_chain = rag_chain
        self.query_formulation_chain = query_formulation_chain
        self.db = db

    def _get_or_create_conversation(self,conversation_id:Optional[int],user_id:int,initial_title:str):
        if conversation_id:
            stmt = select(Conversation).where(Conversation.id==conversation_id,Conversation.user_id==user_id)
            conv = self.db.scalars(stmt).first()
            if conv:
                return conv
        new_conv = Conversation(user_id = user_id,title=initial_title[:40])
        self.db.add(new_conv)
        self.db.commit()
        self.db.refresh(new_conv)
        return new_conv

    async def ask(self,question,user_id:int,conversation_id:Optional[int]=None,document_id:Optional[int]=None):

        conversation = self._get_or_create_conversation(conversation_id=conversation_id,user_id=user_id,initial_title=question)

        stmt = select(Message).where(Message.conversation_id == conversation.id).order_by(Message.created_at.asc())

        history_records = list(self.db.scalars(stmt).all())

        chat_history = []
        for msg in history_records[-6:]:
            if msg.role == "user":
                chat_history.append(HumanMessage(content=msg.content))
            elif msg.role == "assistant":
                chat_history.append(AIMessage(content=msg.content))

        if chat_history:
            standalone_question = self.query_formulation_chain.invoke({
                "chat_history":chat_history,
                "question":question
            })
        else:
            standalone_question = question

        
        docs = self.retriever.retrieve(question=standalone_question,user_id=user_id,document_id=document_id)

        meta_payload = {
            "type": "metadata",
            "conversation_id": conversation.id
        }
        yield f"data: {json.dumps(meta_payload)}\n\n"

        context="\n\n".join(
            doc.page_content
            for doc in docs
            )
        accumulated_answer = []

        async for chunk in self.rag_chain.astream({
            "context":context,
            "chat_history":chat_history,
            "question":question
        }):
            token = chunk.content if hasattr(chunk,"content") else str(chunk)
            accumulated_answer.append(token)
            token_payload = {"type":"token","content":token}
            yield f"data: {json.dumps(token_payload)}\n\n"

        full_response_text = "".join(accumulated_answer)

        user_msg = Message(conversation_id=conversation.id,role="user",content=question)
        ai_msg = Message(conversation_id=conversation.id,role="assistant",content=full_response_text)
        self.db.add_all([user_msg,ai_msg])
        self.db.commit()

        # return({
        #     "conversation_id":conversation.id,
        #     "answer":answer
        # })
        yield "data: [DONE]\n\n"

    def get_conversations(self,user_id:int):
        stmt = select(Conversation).where(Conversation.user_id == user_id).order_by(Conversation.created_at.desc())
        converstations = self.db.scalars(stmt).all()
        return converstations

    def get_conversation_messages(self,user_id:int,conversation_id:int):
        stmt = select(Conversation).where(Conversation.user_id == user_id,Conversation.id == conversation_id)
        conversation = self.db.scalars(stmt).first()
        if not conversation:
            raise HTTPException(detail="Conversation not found or access denied.",status_code=status.HTTP_404_NOT_FOUND)

        msg_stmt = select(Message).where(Message.conversation_id== conversation_id).order_by(Message.created_at.asc())
        messages = self.db.scalars(msg_stmt).all()
        return messages