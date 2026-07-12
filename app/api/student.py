from fastapi import APIRouter, Depends
from app.utils.auth import get_current_student
from app.services.student_service import StudentService

router = APIRouter()


@router.get("/student")
def get_student(current_student: dict = Depends(get_current_student)):
    student_id = current_student["student_id"]
    return StudentService.get_student(student_id)