from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from app.auth.service import AuthService
from app.db.db import get_db
from app.schemas.auth import LoginRequest,RegisterRequest,TokenResponse
from app.auth.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/auth",tags=["Authentication"])

auth_service = AuthService()

@router.post("/register",status_code=status.HTTP_201_CREATED)
def register(request:RegisterRequest,db: Session = Depends(get_db)):
    try:
        user = auth_service.register(db=db,name=request.name,email=request.email,password=request.password)
        return {
            "id": user.id,
            "email":user.email
        }
    except ValueError as exc:
        raise HTTPException(status_code=400,detail=str(exc))

@router.post("/login",response_model=TokenResponse)
def login(request:LoginRequest,db: Session = Depends(get_db)):
    user = auth_service.authenticate(db=db,email=request.email,password=request.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid email or password.")
    return auth_service.create_tokens(user)

@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "id":current_user.id,
        "name":current_user.name,
        "email":current_user.email
    }