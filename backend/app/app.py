from fastapi import FastAPI
from app.routers.auth import router as auth_router
from app.routers.chat import router as chat_router
from app.routers.documents import router as documents_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(documents_router)

@app.get("/")
def health():
    return {
        "status":"online"
    }