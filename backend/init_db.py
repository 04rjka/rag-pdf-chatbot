from app.db.db import engine
from app.db.base import Base

from app.models.user import User
from app.models.document import Document
from app.models.chat import Conversation,Message


Base.metadata.create_all(bind=engine)

print("Database initialized.")