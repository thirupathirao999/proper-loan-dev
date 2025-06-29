from pydantic import BaseModel, EmailStr
from typing import Optional

class Student(BaseModel):
    name: str
    email: str
    password: str
    age: int
    qualification: str
    course: Optional[str] = None

class LoginRequest(BaseModel):
    email: str
    password: str

class CourseAllotment(BaseModel):
    email: str
    course: str