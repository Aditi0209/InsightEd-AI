from fastapi import APIRouter, Depends
from app.agents.feedback_agent import FeedbackAgent
from app.utils.auth import get_current_student

router = APIRouter()

agent = FeedbackAgent()


@router.get("/feedback")
def feedback(current_student: dict = Depends(get_current_student)):
    student_id = current_student["student_id"]
    return agent.generate_feedback(student_id)