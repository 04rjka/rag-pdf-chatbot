from pathlib import Path
from uuid import uuid4
from app.config import settings
from fastapi import UploadFile

class DocumentService:
    def __init__(self, ingestion_service):
        self.ingestion_service = ingestion_service
        self.upload_dir = Path(settings.upload_path)

        self.upload_dir.mkdir(parents=True,exist_ok=True)

    async def upload(self, file: UploadFile):
        if file.content_type != "application/pdf":
            raise ValueError("Only PDF files are allowed.")

        file_id = uuid4()
        filename = f"{file_id}.pdf"
        file_path = self.upload_dir / filename

        contents = await file.read()

        with open(file_path,"wb") as buffer:
            buffer.write(contents)

        result = self.ingestion_service.ingest(str(file_path))

        return({
            "id": str(file_id),
            "filename":file.filename,
            "path":str(file_path),
            "ingestion":result
        })