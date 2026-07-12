from fastapi import APIRouter
from app.services.auth_service import register_student, login_student
from app.models.auth import StudentRegister, StudentLogin, TokenResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register")
async def register(student_data: StudentRegister):
    return register_student(student_data)


@router.post("/login", response_model=TokenResponse)
async def login(login_data: StudentLogin):
    return login_student(login_data.email, login_data.password)
