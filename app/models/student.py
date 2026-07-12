from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional
from datetime import datetime, UTC


class Student(BaseModel):
    student_id: str
    name: str
    email: EmailStr
    hashed_password: str
    student_class: str
    target_exam: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
