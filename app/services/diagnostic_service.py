from app.database.collections import (
    student_profiles_collection
)


class DiagnosticService:

    @staticmethod
    def save_profile(profile):

        student_profiles_collection.update_one(
            {
                "student_id": profile["student_id"]
            },
            {
                "$set": profile
            },
            upsert=True
        )

        return True

    @staticmethod
    def get_profile(student_id):

        return student_profiles_collection.find_one(
            {
                "student_id": student_id
            },
            {
                "_id": 0
            }
        )