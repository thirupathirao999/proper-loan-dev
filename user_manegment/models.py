from pydantic import BaseModel,EmailStr
from typing import Optional

class RegisterUser(BaseModel):
    email: str
    phone: str
    password: str
    first_name: str
    last_name: str
    dob: str
    doj: str
    address: str
    comment: Optional[str] = None
    active: Optional[str] = None


class LoginUser(BaseModel):
    username: str
    password: str

class ChangePassword(BaseModel):
    old_password: str
    new_password: str

class ForgotPassword(BaseModel):
    email:EmailStr
    

class ResetPassword(BaseModel):
    token:str
    new_password: str

class LogoutUser(BaseModel):
    username: str