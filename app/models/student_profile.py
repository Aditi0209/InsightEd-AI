from pydantic import BaseModel
from typing import List


class StudentProfile(BaseModel):
    student_id: str

    confidence_level: str

    study_hours_per_day: int

    academic_goal: str

    preferred_learning_style: str

    self_feedback: str

    strengths: List[str]

    weaknesses: List[str]

    learning_style: str

    risks: List[str]