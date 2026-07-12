from collections import defaultdict

from app.services.performance_service import PerformanceService


class AnalyticsService:

    @staticmethod
    def generate_performance_summary(
        student_id: str
    ):

        tests = PerformanceService.get_student_tests(
            student_id
        )

        if not tests:

            return {
                "message": "No test data found"
            }

        subject_scores = defaultdict(list)

        total_score = 0
        total_tests = 0

        for test in tests:

            score_percentage = (
                test["score"] /
                test["max_score"]
            ) * 100

            subject_scores[
                test["subject"]
            ].append(score_percentage)

            total_score += score_percentage
            total_tests += 1

        average_score = round(
            total_score / total_tests,
            2
        )

        subject_averages = {}

        for subject, scores in subject_scores.items():

            subject_averages[subject] = round(
                sum(scores) / len(scores),
                2
            )

        strongest_subject = max(
            subject_averages,
            key=subject_averages.get
        )

        weakest_subject = min(
            subject_averages,
            key=subject_averages.get
        )

        recent_tests = tests[-5:]

        recent_performance = []

        for test in recent_tests:

            recent_performance.append(
                {
                    "subject": test["subject"],
                    "score_percentage": round(
                        (
                            test["score"]
                            /
                            test["max_score"]
                        ) * 100,
                        2
                    )
                }
            )

        return {
            "student_id": student_id,

            "average_score": average_score,

            "strongest_subject":
            strongest_subject,

            "weakest_subject":
            weakest_subject,

            "subject_averages":
            subject_averages,

            "total_tests":
            total_tests,

            "subject_test_counts":
            {
                subject: len(scores)
                for subject, scores
                in subject_scores.items()
            },

            "recent_performance":
            recent_performance
        }