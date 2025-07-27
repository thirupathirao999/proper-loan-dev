from datetime import datetime, timedelta
from jose import jwt
from dbconnection import db
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from exception import InvalidResetTokenError
from service import get_user_by_email

SECRET = "your-secret-key"
ALGO = "HS256"


oauth2 = OAuth2PasswordBearer(tokenUrl="/loginuser")




def create_access_token(email: str, expires_minutes: int) -> str:
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    return jwt.encode({"sub": email, "exp": expire}, SECRET, algorithm=ALGO)

def decode_access_token(token: str) -> dict:
    return jwt.decode(token, SECRET, algorithms=ALGO)

def create_reset_token(sub: str) -> str:
    expire = datetime.utcnow() + timedelta(hours=1)
    return jwt.encode({"sub": sub, "type": "reset", "exp": expire}, SECRET, algorithm=ALGO)

revoked_tokens = db.revoked_tokens  # Create collection

async def blacklist_token(token: str, exp: int):
    await revoked_tokens.insert_one({"token": token, "exp": datetime.utcfromtimestamp(exp)})

async def is_token_blacklisted(token: str) -> bool:
    exists = await revoked_tokens.find_one({"token": token})
    return exists is not None

async def get_current_user(token: str = Depends(oauth2)):
    data = decode_access_token(token)
    #     if await is_token_blacklisted(token):
    #         raise HTTPException(401, "Token has been revoked.")
    # except JWTError:
    #     raise HTTPException(401, "Invalid token")
    
    user = await get_user_by_email(data.get("sub"))
    if not user:
        raise InvalidResetTokenError()
    # if not user or not user.get("active"):
    #     raise HTTPException(403, "User is inactive.")
    return user