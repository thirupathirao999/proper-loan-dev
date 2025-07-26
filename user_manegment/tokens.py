from datetime import datetime, timedelta
from jose import jwt

SECRET = "your-secret-key"
ALGO = "HS256"

def create_access_token(sub: str, expires_minutes: int) -> str:
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    return jwt.encode({"sub": sub, "exp": expire}, SECRET, algorithm=ALGO)

def decode_access_token(token: str) -> dict:
    return jwt.decode(token, SECRET, algorithms=[ALGO])