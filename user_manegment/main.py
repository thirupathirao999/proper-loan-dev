from datetime import datetime, timedelta
from fastapi import FastAPI
from exception import InvalidCredentialsError, PasswordExpiredError, PasswordPolicyError, UserAlreadyExitsError
from models import  LoginUser, RegisterUser
from dbconnection import user_collection
from password import password_valid, verify_password
from service import get_user, get_user_by_email, register_user
from tokens import create_access_token



app=FastAPI()

users=user_collection
ACCESS_TOKEN_EXPIRE_MINUTES = 60  

@app.post("/registeruser")
async def register(data: RegisterUser):
    user=await get_user_by_email(data.email,data.phone)
    if user:
        raise UserAlreadyExitsError()
    pwd = password_valid(data.password)
    if not pwd:
        raise PasswordPolicyError()
    result = await register_user(data)
    if not result:
        return {"message": "Internal server error.","code":400}
    name= data.first_name + data.last_name
    return {"code":200,"message": f"{name } was register successfully."}


@app.post("/loginuser")
async def login(data:LoginUser):
    user=await get_user(data.username,data.password)
    if not user:
        raise InvalidCredentialsError()
    if datetime.utcnow() - user["password_changed_at"] > timedelta(days=30):
        raise PasswordExpiredError()
    token = create_access_token(user["email"],ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "message":f"{data.username}was login successfully",
        "access_token": token, 
        "token_type": "bearer"
        }
    