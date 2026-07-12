from typing import List, Dict, Any
from pydantic import BaseModel, Field

class StudentMemory(BaseModel):

    student_id: str

    learning_style: str = ""

    academic_goal: str = ""

    weak_subject: str = ""

    strong_subject: str = ""

    confidence_level: str = ""

    strengths: List[str] = Field(default_factory=list)

    weaknesses: List[str] = Field(default_factory=list)

    recent_topics: List[str] = Field(default_factory=list)

    recent_questions: List[str] = Field(default_factory=list)

    last_feedback: str = ""

    last_study_plan: str = ""

    last_performance_summary: Dict[str, Any] = Field(default_factory=dict)