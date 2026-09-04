from datetime import datetime,timedelta,timezone
from pwdlib import PasswordHash
import jwt
from app.config import settings

password_hash = PasswordHash.recommended()

def hash_password(password:str):
    return password_hash.hash(password)

def verify_password(password:str,hashed_password:str):
    return password_hash.verify(password,hashed_password)

def create_access_token(user_id:int):

    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)

    payload = {
        "sub": str(user_id),
        "type":"access",
        "exp": expire
    }
    return jwt.encode(payload,settings.secret_key,algorithm="HS256")

def create_refresh_token(user_id:str):
    
    expire = datetime.now(timezone.utc) + timedelta(days=settings.refresh_token_expire_days)

    payload = {
        "sub": str(user_id),
        "type": "refresh",
        "exp": expire
    }

    return jwt.encode(payload,settings.secret_key,algorithm="HS256")