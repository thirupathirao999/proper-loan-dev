from venv import logger
from fastapi import HTTPException
from Database.dbconnection import user_collection
from datetime import datetime
import re

from utils.exception import InvalidCredentialsError, PhoneNumberError, TooManyResetRequestsError
from security.password import hash_password, verify_password

async def get_user_by_email(email: str):
    return await user_collection.find_one({"$or": [{"email": email}, {"phone":email}]})

def is_valid_phone(phone: str) -> bool:
    return bool(re.fullmatch(r"\d{10}", phone))

async def register_user(data):
    hashed = hash_password(data.password)
    user = data.dict()
    phone=is_valid_phone(data.phone)
    if not phone:
        raise PhoneNumberError()
    user.update({
        "password": hashed,
        "password_changed_at": datetime.utcnow(),
        "active": data.active,
        "invalid_password_count":0
    })
    return await user_collection.insert_one(user)

async def get_user(username,password):
    user = await user_collection.find_one({"$or": [{"email": username}, {"phone": username}]})
    if not user or not verify_password(password, user["password"]):
        user_collection.update_one({"email": user["email"]},{"$inc": {"invalid_password_count":1}})
        if user["invalid_password_count"]>=3:
            logger.error(f" The user {user["email"]} exiceded the inavalid password count")
            raise TooManyResetRequestsError()
        logger.error(f"user:-{user.email} entered invalid username or password")
        raise InvalidCredentialsError()
        #raise InvalidCredentialsError()
    return user



