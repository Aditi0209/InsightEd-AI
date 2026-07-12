from app.services.analytics_service import AnalyticsService
from app.services.diagnostic_service import DiagnosticService


class FeedbackService:

    @staticmethod
    def generate_feedback(student_id: str):

        summary = AnalyticsService.generate_performance_summary(
            student_id
        )

        if "message" in summary:
            return summary

        profile = DiagnosticService.get_profile(student_id)

        if not profile:

            profile = {
                "weaknesses": [],
                "learning_style": "Unknown"
            }

        weakest_subject = summary["weakest_subject"]
        strongest_subject = summary["strongest_subject"]
        average_score = summary["average_score"]

        feedback = {
            "weak_subject_insight": (
                f"{weakest_subject} requires consistent practice "
                f"aligned with your learning profile."
            ),

            "strength_insight": (
                f"Leverage your strength in {strongest_subject} "
                f"to balance overall performance."
            ),

            "performance_insight": (
                "Performance is "
                + ("strong" if average_score > 80 else
                   "moderate" if average_score > 60 else
                   "weak")
            ),

            "study_focus": [
                weakest_subject,
                "Concept revision",
                "Practice questions"
            ],

            "general_advice": [
                "Review mistakes after tests",
                "Practice daily",
                "Take weekly mock tests"
            ]
        }

        return {
            "student_id": student_id,
            "feedback": feedback
        }