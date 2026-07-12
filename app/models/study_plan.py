from pydantic import BaseModel, Field
from datetime import datetime
from typing import List


class StudyPlan(BaseModel):
    student_id: str
    weekly_tasks: List[str]
    generated_at: datetime = Field(default_factory=datetime.utcnow)