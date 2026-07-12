from app.services.feedback_service import FeedbackService
from app.services.analytics_service import AnalyticsService
from app.services.student_service import StudentService
from app.services.diagnostic_service import DiagnosticService
from app.services.memory_service import MemoryService
from app.utils.llm import get_llm


class FeedbackAgent:

    def generate_feedback(
        self,
        student_id: str,
        performance_data: dict = None,
        planner_data: dict = None
    ):

        # ----------------------------------------
        # Student Information
        # ----------------------------------------

        student = StudentService.get_student(
            student_id
        )

        if not student:

            return {
                "message": "Student not found"
            }

        # ----------------------------------------
        # Reuse previous agent outputs
        # ----------------------------------------

        if performance_data:

            summary = performance_data.get(
                "performance_summary",
                {}
            )

            profile = performance_data.get(
                "diagnostic_profile",
                {}
            )

        else:

            summary = AnalyticsService.generate_performance_summary(
                student_id
            )

            profile = DiagnosticService.get_profile(
                student_id
            )

        if planner_data:

            study_plan = planner_data.get(
                "study_plan",
                ""
            )

        else:

            study_plan = "No personalized study plan available."

        # ----------------------------------------
        # Existing feedback signal
        # ----------------------------------------

        feedback_data = FeedbackService.generate_feedback(
            student_id
        )

        if not profile:

            profile = {

                "strengths": [],

                "weaknesses": [],

                "learning_style": "Unknown",

                "confidence_level": "Unknown",

                "academic_goal": "General Improvement",

                "risks": []

            }

        # ----------------------------------------
        # LLM Prompt
        # ----------------------------------------

        prompt = f"""
You are an expert academic mentor and behavioral learning coach.

Generate highly personalized feedback for the student.

You MUST combine:

- Historical academic performance
- Diagnostic profile
- Personalized study plan
- Previous feedback signals

Do NOT generate generic advice.

==================================================

STUDENT

Name:
{student["name"]}

Class:
{student["student_class"]}

Target Exam:
{student["target_exam"]}

==================================================

PERFORMANCE SUMMARY

Average Score:
{summary.get("average_score","")}

Strongest Subject:
{summary.get("strongest_subject","")}

Weakest Subject:
{summary.get("weakest_subject","")}

Subject Averages:
{summary.get("subject_averages",{})}

==================================================

DIAGNOSTIC PROFILE

Strengths:
{profile.get("strengths",[])}

Weaknesses:
{profile.get("weaknesses",[])}

Learning Style:
{profile.get("learning_style","")}

Confidence Level:
{profile.get("confidence_level","")}

Academic Goal:
{profile.get("academic_goal","")}

Risks:
{profile.get("risks",[])}

==================================================

CURRENT STUDY PLAN

{study_plan}

==================================================

SYSTEM FEEDBACK SIGNAL

{feedback_data.get("feedback","")}

==================================================

INSTRUCTIONS

- Explain why the student is facing difficulties.
- Connect weaknesses with the current study plan.
- Mention strengths that should be leveraged.
- Focus only on the highest-priority improvements.
- Suggest realistic actions that can be completed within one week.
- Adapt every recommendation to the student's learning style.
- Encourage the student if confidence is low.
- Do NOT repeat performance statistics already provided.
- Use previous feedback only if it is still relevant.
- Give practical, actionable advice instead of theory.

IMPORTANT RESPONSE RULES

- Maximum 250 words.
- Use short headings.
- Use bullet points only.
- Do NOT write long paragraphs.
- Each bullet should be one concise sentence.
- Maximum 3 bullets under each section.
- Keep the response suitable for display inside a web application.
- Avoid unnecessary explanations or repetition.

OUTPUT FORMAT

## Encouragement
• Mention 1–2 positive observations.

## Current Status
• Current academic situation.
• Biggest challenge.

## Priority Improvements
• Top 3 improvement areas.

## This Week's Action Plan
• 3–5 practical tasks for this week.

## Motivation
• End with one short encouraging message.
"""

        response = get_llm().invoke(prompt)

        # ----------------------------------------
        # Update Long-Term Student Memory
        # ----------------------------------------
        
        MemoryService.update_memory(
            student_id,
            {
                "weak_subject": summary.get("weakest_subject", ""),
                "strong_subject": summary.get("strongest_subject", ""),
                "average_score": summary.get("average_score", 0),
                "learning_style": profile.get("learning_style", ""),
                "confidence_level": profile.get("confidence_level", ""),
                "academic_goal": profile.get("academic_goal", ""),
                "strengths": profile.get("strengths", []),
                "weaknesses": profile.get("weaknesses", []),
                "last_feedback": response.content
            }
        )

        return {

            "student_id": student_id,

            "feedback": response.content,

            "performance_summary": summary,

            "diagnostic_profile": profile,

            "study_plan": study_plan

        }