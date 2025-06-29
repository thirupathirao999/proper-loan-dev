from helpers import load_students,save_students
from logger import get_logger
from fastapi import FastAPI, HTTPException
import asyncio




# Initialize logger
logger = get_logger(__name__)

async def register_student(data):
    students = load_students()
    new_student = data.dict()
    for s in students:
        if s["email"] == new_student["email"]:
            logger.warning(f'Registration failed: Email already registered - {new_student["email"]}')
            raise HTTPException(status_code=400, detail="Email already registered.")
    
    students.append(new_student)
    save_students(students) 

    logger.info(f'Registered new student: {new_student["email"]}')
    return {"message": f"Registration successful for {new_student['email']}"}



async def login_student(data):
    students = load_students()
    for student in students:
        if student["email"] == data.email and student["password"] == data.password:
            logger.info(f"Login successful: {data.email}")
            return {"message": f"Login successful for  {data.email} "}

    logger.warning(f"Login failed: Invalid credentials - {data.email}")
    raise HTTPException(status_code=401, detail="Invalid credentials")






async def student_allot_course(data):
    students = load_students()
    for student in students:
        if student["email"] == data.email:
            if student["course"] == data.course:
                logger.info(f"{data.email} already enrolled in: {data.course}")
                raise HTTPException(status_code=400, detail=f"{data.email} already enrolled in: {data.course}")
            
            student["course"] = data.course
            for i, s in enumerate(students):
                if s["email"] == data.email:
                    students[i] = student
            save_students(students)
            #save_students(students)  # Do NOT append again
            logger.info(f"Course allotted: {data.course} to {data.email}")
            return {"message": f"Course '{data.course}' allotted to {student['name']}"}

    logger.warning(f"Allotment failed: Student not found - {data.email}")
    raise HTTPException(status_code=404, detail="Student not found")


async def students_by_course(course_name):
    students = load_students()
    filtered_students = [s for s in students if s["course"] == course_name]
    return filtered_students