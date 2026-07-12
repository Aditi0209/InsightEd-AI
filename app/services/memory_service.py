from app.database.collections import student_memory_collection


class MemoryService:

    @staticmethod
    def get_memory(student_id: str):

        memory = student_memory_collection.find_one(
            {"student_id": student_id},
            {"_id": 0}
        )

        if not memory:
            return {}

        return memory

    @staticmethod
    def update_memory(
        student_id: str,
        updates: dict
    ):

        student_memory_collection.update_one(
            {
                "student_id": student_id
            },
            {
                "$set": updates,
                "$setOnInsert": {
                    "student_id": student_id
                }
            },
            upsert=True
        )

        return True