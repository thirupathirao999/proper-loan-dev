from datetime import datetime, timedelta, timezone
from http.client import HTTPException
from jose import jwt
from Database.dbconnection import db,revoked_tokens
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from utils.exception import AccessDeniedError, InvalidResetTokenError, TokenBlocklistError
from utils.service import get_user_by_email



ACCESS_TOKEN_EXPIRE_MINUTES = 60
SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
oauth2 = OAuth2PasswordBearer(tokenUrl="/loginuser")




def role_required(required_role: str):
    def wrapper(token: str = Depends(oauth2)):
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_exp": False})
        exp = payload.get("exp")
        if datetime.now(timezone.utc).timestamp() > exp:
            raise InvalidResetTokenError()
        if not payload:
            raise InvalidResetTokenError()
        user_role = payload.get("role")
        if user_role != required_role:
            raise AccessDeniedError()
        return payload
    return wrapper


# def create_access_token(email: str, expires_minutes: int) -> str:
#     expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
#     return jwt.encode({"sub": email, "exp": expire}, SECRET, algorithm=ALGO)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)

# def create_reset_token(sub: str) -> str:
#     expire = datetime.utcnow() + timedelta(hours=1)
#     return jwt.encode({"sub": sub, "type": "reset", "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)

 

async def blacklist_token(token: str, exp: int):
    await revoked_tokens.insert_one({"token": token, "exp": datetime.utcfromtimestamp(exp)})

async def is_token_blacklisted(token: str) -> bool:
    exists = await revoked_tokens.find_one({"token": token})
    return exists 

async def get_current_user(token: str = Depends(oauth2)):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_exp": False})
    exp = payload.get("exp")
    if datetime.now(timezone.utc).timestamp() > exp:
        raise InvalidResetTokenError()
    if await is_token_blacklisted(token):
        raise TokenBlocklistError()
    expire_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

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
    