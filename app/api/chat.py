from fastapi import APIRouter, Depends
from app.agents.supervisor import SupervisorAgent
from app.utils.auth import get_current_student

router = APIRouter()

supervisor = SupervisorAgent()


@router.post("/chat")
def chat(
    query: str,
    current_student: dict = Depends(get_current_student)
):
    student_id = current_student["student_id"]
    result = supervisor.route_query(
        query=query,
        student_id=student_id
    )
    return result