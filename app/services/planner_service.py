from app.models.study_plan import StudyPlan
from app.database.collections import study_plans_collection


class PlannerService:

    @staticmethod
    def generate_study_plan(
        student_id: str,
        performance_summary: dict
    ):

        weakest_subject = performance_summary.get(
            "weakest_subject",
            "General Revision"
        )

        strongest_subject = performance_summary.get(
            "strongest_subject",
            "General Practice"
        )

        average_score = performance_summary.get(
            "average_score",
            0
        )

        if average_score >= 85:

            intensity = "Maintain and strengthen"

        elif average_score >= 65:

            intensity = "Moderate Improvement"

        else:

            intensity = "High Improvement"

        study_plan = StudyPlan(

            student_id=student_id,

            weekly_tasks=[

                f"Priority Subject: {weakest_subject}",

                f"Strength to Maintain: {strongest_subject}",

                f"Study Intensity: {intensity}",

                "Focus on concept clarity",

                "Practice previous mistakes",

                "Attempt one mock test this week",

                "Revise important formulas and notes"

            ]

        )

        study_plans_collection.insert_one(

            study_plan.model_dump()

        )

        return study_plan

    @staticmethod
    def get_study_plans(
        student_id: str
    ):

        plans = list(

            study_plans_collection.find(

                {
                    "student_id": student_id
                }

            )

        )

        for plan in plans:

            plan.pop("_id", None)

        return plans