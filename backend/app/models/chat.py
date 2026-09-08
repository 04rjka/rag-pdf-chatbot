from __future__ import annotations
from datetime import datetime,timezone
from sqlalchemy import String,Integer,DateTime,ForeignKey,Text
from sqlalchemy.orm import Mapped,mapped_column,relationship
from app.db.db import Base

class Conversation(Base):
    __tablename__ = "conversations"
    id:Mapped[int] = mapped_column(primary_key=True,index=True)
    user_id:Mapped[int] = mapped_column(ForeignKey("users.id",ondelete="cascade"),index=True,nullable=False)
    title:Mapped[str] = mapped_column(String(255),nullable=False,default="New chat")
    created_at:Mapped[DateTime]= mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc),nullable=False)
    user: Mapped[User] = relationship(back_populates="conversations")
    messages: Mapped[list[Message]] = relationship(back_populates="conversation",cascade="all, delete-orphan",order_by="Message.created_at")

class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    conversation_id: Mapped[int] = mapped_column(ForeignKey("conversations.id", ondelete="CASCADE"),index=True,nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),default=lambda: datetime.now(timezone.utc),nullable=False)

    conversation: Mapped[Conversation] = relationship(back_populates="messages")