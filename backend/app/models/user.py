from sqlalchemy import String,Boolean
from sqlalchemy.orm import Mapped,mapped_column,relationship
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255),unique=True,index=True,nullable=False)
    name:  Mapped[str] = mapped_column(String(255),nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255),nullable=False)
    is_active:  Mapped[bool] = mapped_column(Boolean,default=True,nullable=False)

    documents = relationship("Document",back_populates="user",cascade="all, delete-orphan")