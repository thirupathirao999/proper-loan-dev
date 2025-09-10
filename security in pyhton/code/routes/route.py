from datetime import datetime, timedelta
from utils.logs import logger
from fastapi import APIRouter, Depends, Request
from utils.exception import (InvalidCredentialsError, InvalidResetTokenError,  
                       PasswordExpiredError, 
                       PasswordIncorrectError, 
                       PasswordMatchError, 
                       PasswordPolicyError, TokenBlocklistError, 
                       TooManyResetRequestsError,
                        UserAlreadyExitsError, 
                        UserNotExitsError)
from routes.models import  ChangePassword, LoginUser, RegisterUser
from Database.dbconnection import user_collection
from security.password import hash_password, password_valid, verify_password
from utils.service import get_user, get_user_by_email, register_user
from security.tokens import blacklist_token, create_access_token, decode_access_token,  get_current_user, get_token_from_header, is_token_blacklisted


router=APIRouter()

users=user_collection


@router.post("/registeruser")
async def register(data: RegisterUser):
    user=await get_user_by_email(data.email)
    if user:
        logger.error(f" The user with this email {data.email} was already existed")
        raise UserAlreadyExitsError()
    pwd = password_valid(data.password)
    if not pwd:
        logger.error(f" The password enter by user :- {data.email} is not a valid")
        raise PasswordPolicyError()
    result = await register_user(data)
    if not result:
        return {"message": "Internal server error.","code":400}
    name= data.first_name + data.last_name
    logger.info(f"{name }  was register successfully.")
    return {"code":200,"message": f"{name }  was register successfully."}


@router.post("/loginuser")
async def login(data:LoginUser):
    user=await get_user(data.username,data.password)
    if not user:
        #user_collection.update_one({"email": user["email"]},{"$inc": {"invalid_password_count":1}})
        if user["invalid_password_count"]>=3:
            logger.error(f" The user {data.customer_id} exiceded the inavalid password count")
            raise TooManyResetRequestsError()
        logger.error(f"user:-{user.email} entered invalid username or password")
        raise InvalidCredentialsError()
    if datetime.utcnow() - user["password_changed_at"] > timedelta(days=30):
        raise PasswordExpiredError()
    await user_collection.update_one({"_id": user["_id"]},{"$set": {"active": "True"}})
    #token = create_access_token(user["email"],ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token({"sub": user["email"], "role": user["role"]})
    logger.info(f"{data.username }  was login successfully.")
    return {
        "message":f"{data.username} was login successfully",
        "access_token": token, 
        "token_type": "bearer"
        }


@router.post("/changepassword")
async def changepassword(data:ChangePassword,user=Depends(get_current_user)):
    password=verify_password(data.old_password, user["password"])

    if user["invalid_password_count"]>=3 and ((datetime.utcnow() - user["password_changed_at"])>timedelta(minutes=60)):
         await user_collection.update_one({"_id": user["_id"]},{"$set": {"invalid_password_count":0}})

    if not password:
        user_collection.update_one({"_id": user["_id"]},{"$inc": {"invalid_password_count":1}})
        if user["invalid_password_count"]>=3:
            logger.error(f" The user {data.customer_id} exiceded the inavalid password count")
            raise TooManyResetRequestsError()
        raise PasswordIncorrectError()
    if user["invalid_password_count"]<=3:   
        pwd = password_valid(data.new_password)
        if not pwd:
            logger.error(f" The new password entered by user {data.customer_id} is not valid")
            raise PasswordPolicyError()
        hashed = hash_password(data.new_password)
    
    
        await user_collection.update_one(
                {"_id": user["_id"]},
                {"$set": {"password": hashed,
                          "password_changed_at": datetime.utcnow()}})
    logger.info(f"{user["email"] }  was changed password successfully.")
    return {"code":200,"message":"password changed successfully"}





@router.post("/logout")
async def logout(request: Request, user=Depends(get_current_user)):
    if not user:
        raise  UserNotExitsError()
    token = get_token_from_header(request)
    if not token:
        raise InvalidResetTokenError()
    blok_token= await is_token_blacklisted(token)
    if blok_token:
        raise TokenBlocklistError() 
    decoded = decode_access_token(token)
    exp = decoded.get("exp")
    ttl = exp - int(datetime.utcnow().timestamp())
    if ttl <= 0:
        raise InvalidResetTokenError()
    
    await blacklist_token(token,exp)
    await user_collection.update_one({"_id": user["_id"]},{"$set": {"active": "Falses"}})
    logger.info(f"{user["email"] }  was logout successfully.")
    return {"message": "Logged out successfully"}
   