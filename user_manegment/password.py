from passlib.context import CryptContext
import re
from datetime import datetime




pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
def password_valid(pw: str):
    return (
        8 <= len(pw) <= 20
        and re.search(r"[A-Z]", pw)
        and re.search(r"[a-z]", pw)
        and re.search(r"\d", pw)
        and re.search(r"[^\w\s]", pw)
    )

def hash_password(pw: str) -> str:
    return pwd_ctx.hash(pw)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_ctx.verify(plain, hashed)