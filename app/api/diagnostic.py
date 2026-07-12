from fastapi import APIRouter, Depends
from app.agents.diagnostic_agent import DiagnosticAgent
from app.utils.auth import get_current_student

router = APIRouter()

agent = DiagnosticAgent()


@router.post("/diagnostic")
def diagnostic(
    confidence_level: str,
    study_hours_per_day: int,
    academic_goal: str,
    preferred_learning_style: str,
    self_feedback: str,
    current_student: dict = Depends(get_current_student)
):
    student_id = current_student["student_id"]
    return agent.analyze(
        student_id,
        confidence_level,
        study_hours_per_day,
        academic_goal,
        preferred_learning_style,
        self_feedback
    )