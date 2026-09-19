from fastapi import APIRouter,Depends,HTTPException,status,Response,Cookie
from sqlalchemy.orm import Session
from app.auth.service import AuthService
from app.db.db import get_db
from app.schemas.auth import LoginRequest,RegisterRequest,TokenResponse,RefreshTokenRequest
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.config import settings

router = APIRouter(prefix="/auth",tags=["Authentication"])

auth_service = AuthService()

IS_PRODUCTION = False

COOKIE_PARAMS = {
    "httponly": True,
    "samesite": "lax",
    "secure": IS_PRODUCTION,
}

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

@router.post("/login")
def login(request:LoginRequest,response:Response,db: Session = Depends(get_db)):
    user = auth_service.authenticate(db=db,email=request.email,password=request.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid email or password.")
    
    tokens = auth_service.create_tokens(user)

    response.set_cookie(
        key="access_token",
        value=tokens["access_token"],
        max_age=(settings.access_token_expire_minutes * 60),
        **COOKIE_PARAMS
    )
    response.set_cookie(
            key="refresh_token",
            value=tokens["refresh_token"],
            max_age=(settings.refresh_token_expire_days * 1440),
            path="/auth",
            **COOKIE_PARAMS
        )

    return {"message": "Logged in successfully", "user": {"id": user.id, "email": user.email}}

@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "id":current_user.id,
        "name":current_user.name,
        "email":current_user.email
    }

@router.post("/refresh")
def refresh_token(response : Response, refresh_token: str|None = Cookie(default=None),db:Session = Depends(get_db)):
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token missing from cookies"
        )
    
    new_access_token = auth_service.refresh_access_token(refresh_token=refresh_token,db=db)

    response.set_cookie(
            key="access_token",
            value=new_access_token,
            max_age=(settings.access_token_expire_minutes * 60),
            **COOKIE_PARAMS
        )
    return {"message": "Token refreshed successfully"}