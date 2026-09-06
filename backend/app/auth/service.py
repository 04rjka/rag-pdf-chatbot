from sqlalchemy import select
from sqlalchemy.orm import Session
from app.auth.security import create_access_token,create_refresh_token,hash_password,verify_password,decode_token
from app.models.user import User
from fastapi import HTTPException,status

class AuthService:

    def register(self,db:Session,name:str,email:str,password:str):
        existing_user = db.scalar(select(User).where(User.email == email))
        if existing_user:
            raise ValueError("Email is already registered.")

        user = User(email=email,name=name,password_hash=hash_password(password))
        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    def authenticate(self,db:Session,email:str,password:str):
        user = db.scalar(select(User).where(User.email == email))
        if not user:
            return None
        if not verify_password(password,user.password_hash):
            return None
        return user

    def create_tokens(self, user:User):
        return(
            {
                "access_token": create_access_token(user.id),
                "refresh_token": create_refresh_token(user.id),
                "token_type":"bearer"
            }
        )

    def refresh_access_token(self,db: Session,refresh_token:str):
        try:
            payload = decode_token(refresh_token)
        except Exception:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED,detail="Invaild refresh token.")

        if payload.get("type") != "refresh":
            raise HTTPException(status.HTTP_401_UNAUTHORIZED,detail="Invaild token type.")

        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED,detail="Invaild refresh token.")

        user = db.get(User,int(user_id))

        if user is None:
                    raise HTTPException(status.HTTP_401_UNAUTHORIZED,detail="User not found.")

        if not user.is_active:
             raise HTTPException(status.HTTP_403_FORBIDDEN,detail="User account is inactive.")

        return create_access_token(user.id)