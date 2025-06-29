from fastapi import FastAPI, HTTPException
import asyncio
from models import Student,LoginRequest,CourseAllotment
from service import register_student,login_student,student_allot_course,students_by_course
from helpers import load_students
from logger import get_logger
import json
import os

app = FastAPI()


courses = [
    {"name": "python", "duration": "3 months"},
    {"name": "java", "duration": "3 months"},
    {"name": "html", "duration": "4 months"}
]
# Initialize logger
logger = get_logger(__name__)

@app.post("/student-registration")
async def register(data: Student):
    result= await register_student(data)
    return result

@app.post("/login")
async def login(data: LoginRequest):
    result= await login_student(data)
    return result

@app.get("/course_available")
def list_courses():
    return courses

@app.post("/allot-course")
async def allot_course(data: CourseAllotment):
    result=await student_allot_course(data)
    return result

@app.get("/list_all_students")
def get_all_students():
    return load_students()

@app.get("/students_course/{course_name}")
async def get_students_by_course(course_name: str):
    result= await students_by_course(course_name)
    return result