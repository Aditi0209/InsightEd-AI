from app.database.collections import students_collection
from app.models.student import Student


class StudentService:

    @staticmethod
    def create_student(student: Student):

        students_collection.insert_one(
            student.model_dump()
        )

        return {
            "message": "Student created successfully"
        }

    @staticmethod
    def get_student(student_id: str):
        student = students_collection.find_one(
            {"student_id": student_id}
        )

        if not student:
            return {
                "message": "Student not found"
            }

        student.pop("_id", None)
        student.pop("hashed_password", None)

        return student