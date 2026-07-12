from fastapi import APIRouter, Depends
from app.agents.planner_agent import PlannerAgent
from app.utils.auth import get_current_student

router = APIRouter()

agent = PlannerAgent()


@router.get("/planner")
def study_plan(current_student: dict = Depends(get_current_student)):
    student_id = current_student["student_id"]
    return agent.generate_personalized_plan(student_id)