from datetime import datetime, timedelta
from jose import jwt, JWTError
from app.config import Config

def generate_access_token(data: dict) -> str:
    try:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, Config.SECRET_KEY, algorithm=Config.ALGORITHM)
        return encoded_jwt
    except JWTError as e:
        print(f"JWT encoding error: {e}")
        return ""