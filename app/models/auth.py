from pydantic import BaseModel, Field
from typing import Optional


class StudentRegister(BaseModel):
    student_id: str
    name: str
    email: str
    password: str
    student_class: str
    target_exam: Optional[str] = None


class StudentLogin(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    student_id: str
    name: str
