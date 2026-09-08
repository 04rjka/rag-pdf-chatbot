from pathlib import Path
from uuid import uuid4
from app.config import settings
from fastapi import UploadFile,HTTPException,status
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.user import User
from app.models.document import Document
from app.services.ingestion_service import IngestionService

class DocumentService:
    def __init__(self,db:Session, ingestion_service:IngestionService):
        self.db = db
        self.ingestion_service = ingestion_service
        self.upload_dir = Path(settings.upload_path)
        self.upload_dir.mkdir(parents=True,exist_ok=True)

    async def upload(self, file: UploadFile,current_user:User):
        if file.content_type != "application/pdf":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Only PDF files are allowed.")

        user_folder = self.upload_dir / str(current_user.id)
        user_folder.mkdir(parents=True,exist_ok=True)

        display_name = Path(file.filename).name
        file_id = uuid4()
        stored_filename = f"{file_id}.pdf"
        file_path = user_folder / stored_filename

        contents = await file.read()

        try:
            with open(file_path,"wb") as buffer:
                buffer.write(contents)
        except Exception as exc:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"Failed to write file to disk : {str(exc)}")

        db_document = Document(user_id = current_user.id,filename = display_name,file_path = str(file_path),)

        try:
            self.db.add(db_document)
            self.db.commit()
            self.db.refresh(db_document)
        except Exception as exc:
            self.db.rollback()
            if file_path.exists():
                file_path.unlink()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"Database commit failed : {str(exc)}")

        result = self.ingestion_service.ingest(str(file_path),user_id=current_user.id,document_id=db_document.id)

        return db_document

    def get_user_documents(self,user_id:int):
        stmt = select(Document).where(Document.user_id == user_id).order_by(Document.created_at.desc())
        return self.db.scalars(stmt).all()