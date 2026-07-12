from fastapi import APIRouter, Depends
from app.models.test_result import TestResult
from app.services.performance_service import PerformanceService
from app.utils.auth import get_current_student

router = APIRouter()


@router.post("/test")
def add_test(test_result: TestResult, current_student: dict = Depends(get_current_student)):
    student_id = current_student["student_id"]
    test_result.student_id = student_id
    return PerformanceService.add_test_result(test_result)