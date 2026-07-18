from app.rag.pdf_loader import load_pdf
from app.rag.chunking import split_documents
from app.rag.vector_store import create_db
from pathlib import Path
from app.config import settings

# UPLOAD_DIR = Path(__file__).resolve().parent.parent / "storage" / "uploads"
# pdf_path = UPLOAD_DIR / "mysql.pdf"

pdf_path = Path(settings.upload_path) / "html.pdf"
documents = load_pdf(str(pdf_path))

print(documents[0])
chunks = split_documents(documents)

db = create_db(chunks)