from fastapi import APIRouter, Depends
from app.agents.performance_agent import PerformanceAgent
from app.utils.auth import get_current_student

router = APIRouter()

agent = PerformanceAgent()


@router.get("/performance")
def performance_report(current_student: dict = Depends(get_current_student)):
    student_id = current_student["student_id"]
    return agent.generate_report(student_id)