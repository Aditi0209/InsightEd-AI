from pydantic import BaseModel, Field
from datetime import datetime


class TestResult(BaseModel):
    student_id: str
    subject: str
    topic: str
    score: float
    max_score: float
    test_date: datetime = Field(default_factory=datetime.utcnow)