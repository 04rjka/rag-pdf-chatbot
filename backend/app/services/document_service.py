from pathlib import Path
from uuid import uuid4
from app.config import settings
from fastapi import UploadFile,HTTPException,status
from sqlalchemy.orm import Session
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

        file_id = uuid4()
        filename = f"{file_id}.pdf"
        file_path = user_folder / filename

        contents = await file.read()

        try:
            with open(file_path,"wb") as buffer:
                buffer.write(contents)
        except Exception as exc:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"Failed to write file to disk : {str(exc)}")

        db_document = Document(user_id = current_user.id,filename = filename,file_path = str(file_path),)

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

        # return({
        #     "id": str(file_id),
        #     "filename":file.filename,
        #     "path":str(file_path),
        #     "ingestion":result
        # })
        return db_document