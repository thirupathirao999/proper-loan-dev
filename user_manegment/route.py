from datetime import datetime, timedelta
from http.client import HTTPException
from fastapi import APIRouter, Depends, FastAPI
from exception import (InvalidCredentialsError,  
                       PasswordExpiredError, 
                       PasswordIncorrectError, 
                       PasswordMatchError, 
                       PasswordPolicyError, 
                       TooManyResetRequestsError,
                        UserAlreadyExitsError, 
                        UserNotExitsError)
from models import  ChangePassword, ForgotPassword, LoginUser, LogoutUser, RegisterUser
from dbconnection import user_collection
from password import hash_password, password_valid, verify_password
from service import get_user, get_user_by_email, register_user
from tokens import create_access_token, create_reset_token, get_current_user



router=APIRouter()

users=user_collection
ACCESS_TOKEN_EXPIRE_MINUTES = 60  
count=0

@router.post("/registeruser")
async def register(data: RegisterUser):
    user=await get_user(data.email,data.phone)
    if user:
        raise UserAlreadyExitsError()
    pwd = password_valid(data.password)
    if not pwd:
        raise PasswordPolicyError()
    result = await register_user(data)
    if not result:
        return {"message": "Internal server error.","code":400}
    name= data.first_name + data.last_name
    return {"code":200,"message": f"{name }  was register successfully."}


@router.post("/loginuser")
async def login(data:LoginUser):
    user=await get_user(data.username,data.password)
    if not user:
        raise InvalidCredentialsError()
    if datetime.utcnow() - user["password_changed_at"] > timedelta(days=30):
        raise PasswordExpiredError()
    await user_collection.update_one({"_id": user["_id"]},{"$set": {"active": "True"}})
    token = create_access_token(user["email"],ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "message":f"{data.username}was login successfully",
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
            raise TooManyResetRequestsError()
        raise PasswordIncorrectError()
    if user["invalid_password_count"]<=3:   
        pwd = password_valid(data.new_password)
        if not pwd:
            raise PasswordPolicyError()
        hashed = hash_password(data.new_password)
    
    
        await user_collection.update_one(
                {"_id": user["_id"]},
                {"$set": {"password": hashed,
                          "password_changed_at": datetime.utcnow()}})
    
    return {"code":200,"message":"password changed successfully"}


@router.post("/forgotpassword")
async def forgot(data: ForgotPassword):
    user= await get_user_by_email(data.username)
    if not user:
        raise  UserNotExitsError()
    password=verify_password(data.new_password, user["password"])
    if password:
        raise PasswordMatchError()
    pwd = password_valid(data.new_password)
    if not pwd:
        raise PasswordPolicyError()
    hashed = hash_password(data.new_password)
    if user["forget_password_count"]>=3 and ((datetime.utcnow() - user["password_changed_at"])>timedelta(minutes=60)):
        await user_collection.update_one({"_id": user["_id"]},{"$set": {"forget_password_count":0}})
    if user["forget_password_count"]<3:
        await user_collection.update_many(
           {"_id": user["_id"]},
             {"$set": {"password": hashed,
                       "password_changed_at": datetime.utcnow()},
             "$inc": {
                 "forget_password_count": 1
             }})
    else:
        raise TooManyResetRequestsError()
    return {"message":"you password is updated go to login page"}


@router.post("/logout")
async def logout(data:LogoutUser):
    # Here you'd blacklist the token or handle session invalidation if needed
    user= await get_user_by_email(data.username)
    if not user:
        raise  UserNotExitsError()
    await user_collection.update_one({"_id": user["_id"]},{"$set": {"active": "Falses"}})
    return {"message":"your loged out . close the appllication"}
