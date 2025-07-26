from pydantic import BaseModel
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
    
