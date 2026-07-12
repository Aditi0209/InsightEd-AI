from app.database.collections import students_collection
from app.models.student import Student
from app.models.auth import StudentRegister
from app.utils.auth import get_password_hash, verify_password, create_access_token
from fastapi import HTTPException, status


def register_student(student_data: StudentRegister):
    if students_collection.find_one({"student_id": student_data.student_id}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student ID already registered"
        )
    if students_collection.find_one({"email": student_data.email}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    hashed_password = get_password_hash(student_data.password)
    student = Student(
        student_id=student_data.student_id,
        name=student_data.name,
        email=student_data.email,
        hashed_password=hashed_password,
        student_class=student_data.student_class,
        target_exam=student_data.target_exam
    )
    students_collection.insert_one(student.model_dump())
    return {"message": "Student registered successfully"}


def login_student(email: str, password: str):
    student = students_collection.find_one({"email": email})
    if not student or not verify_password(password, student["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    access_token = create_access_token(data={"sub": student["student_id"]})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "student_id": student["student_id"],
        "name": student["name"]
    }
