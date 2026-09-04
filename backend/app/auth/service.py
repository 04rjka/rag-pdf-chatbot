from sqlalchemy import select
from sqlalchemy.orm import Session
from app.auth.security import create_access_token,create_refresh_token,hash_password,verify_password
from app.models.user import User

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