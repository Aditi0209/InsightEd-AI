from app.database.collections import test_results_collection
from app.models.test_result import TestResult


class PerformanceService:

    @staticmethod
    def add_test_result(test_result: TestResult):

        test_results_collection.insert_one(
            test_result.model_dump()
        )

        return {
            "message": "Test result added successfully"
        }

    @staticmethod
    def get_student_tests(student_id: str):

        tests = list(
            test_results_collection.find(
                {"student_id": student_id}
            )
        )

        for test in tests:
            test.pop("_id", None)

        return tests

    @staticmethod
    def get_subject_tests(
        student_id: str,
        subject: str
    ):

        tests = list(
            test_results_collection.find(
                {
                    "student_id": student_id,
                    "subject": subject
                }
            )
        )

        for test in tests:
            test.pop("_id", None)

        return tests