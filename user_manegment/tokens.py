from datetime import datetime, timedelta
from http.client import HTTPException
from jose import jwt
from dbconnection import db,revoked_tokens
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, Request
from exception import InvalidResetTokenError, TokenBlocklistError
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

 

async def blacklist_token(token: str, exp: int):
    await revoked_tokens.insert_one({"token": token, "exp": datetime.utcfromtimestamp(exp)})

async def is_token_blacklisted(token: str) -> bool:
    exists = await revoked_tokens.find_one({"token": token})
    return exists 

async def get_current_user(token: str = Depends(oauth2)):
    if await is_token_blacklisted(token):
        raise TokenBlocklistError()
    data = decode_access_token(token)
    
    # except JWTError:
    #     raise HTTPException(401, "Invalid token")
    
    user = await get_user_by_email(data.get("sub"))
    if not user:
        raise InvalidResetTokenError()
    # if not user or not user.get("active"):
    #     raise HTTPException(403, "User is inactive.")
    return user


def get_token_from_header(request):
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        return auth_header.split(" ")[1]  # Get just the token part
    raise HTTPException(status_code=401, detail="Invalid or missing token")