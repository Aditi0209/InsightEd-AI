from app.services.planner_service import PlannerService
from app.services.analytics_service import AnalyticsService
from app.services.student_service import StudentService
from app.services.diagnostic_service import DiagnosticService
from app.services.memory_service import MemoryService
from app.utils.llm import get_llm


class PlannerAgent:

    def generate_personalized_plan(
        self,
        student_id: str,
        performance_data: dict = None
    ):

        # ---------------------------------------
        # Student Information
        # ---------------------------------------
        student = StudentService.get_student(
            student_id
        )

        if not student:
            return {
                "message": "Student not found"
            }

        # ---------------------------------------
        # Student Memory
        # ---------------------------------------
        memory = MemoryService.get_memory(
            student_id
        )

        # ---------------------------------------
        # Reuse PerformanceAgent output if available
        # ---------------------------------------
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

        # ---------------------------------------
        # Fallback Profile
        # ---------------------------------------
        if not profile:

            profile = {
                "strengths": [],
                "weaknesses": [],
                "learning_style": "Unknown",
                "confidence_level": "Unknown",
                "academic_goal": "General Improvement",
                "risks": []
            }

        # ---------------------------------------
        # Base Study Plan
        # ---------------------------------------
        plan = PlannerService.generate_study_plan(
            student_id,
            summary
        )

        # ---------------------------------------
        # Prompt
        # ---------------------------------------
        prompt = f"""
You are an expert academic mentor.

Generate a personalized and realistic weekly study plan.

The study plan must consider:

- Historical academic performance
- Student learning style
- Academic goals
- Long-term student memory 
- Previous weaknesses
- Previously successful study strategies

==================================================

STUDENT

Name:
{student["name"]}

Class:
{student["student_class"]}

Target Exam:
{student["target_exam"]}

==================================================

STUDENT MEMORY

{memory}

==================================================

PERFORMANCE SUMMARY

Average Score:
{summary.get("average_score", "")}

Strongest Subject:
{summary.get("strongest_subject", "")}

Weakest Subject:
{summary.get("weakest_subject", "")}

Subject Averages:
{summary.get("subject_averages", {})}

==================================================

DIAGNOSTIC PROFILE

Strengths:
{profile.get("strengths", [])}

Weaknesses:
{profile.get("weaknesses", [])}

Learning Style:
{profile.get("learning_style", "")}

Confidence Level:
{profile.get("confidence_level", "")}

Academic Goal:
{profile.get("academic_goal", "")}

Risks:
{profile.get("risks", [])}

==================================================

BASE STUDY PLAN

{plan.weekly_tasks}

==================================================

INSTRUCTIONS

- Prioritize the weakest subject.
- Allocate more time to weak concepts.
- Reinforce the strongest subject.
- Adapt the schedule according to the student's learning style.
- Consider the student's confidence level.
- Reuse successful study strategies from memory.
- Avoid strategies that previously did not help.
- Include revision sessions.
- Include practice sessions.
- Include one self-assessment during the week.
- Keep the plan realistic.
- Do NOT create an hour-by-hour timetable.
- Keep tasks short and actionable.

IMPORTANT RESPONSE RULES

- Maximum 300 words.
- Use headings and bullet points only.
- Do NOT write paragraphs.
- Keep each bullet to one sentence.
- The response should be suitable for display in a web application.
- Avoid unnecessary explanations.

OUTPUT FORMAT

## Weekly Focus
• Primary subject to improve.
• Main objective for the week.

## Daily Tasks

Monday
• Task 1
• Task 2

Tuesday
• Task 1
• Task 2

Wednesday
• Task 1
• Task 2

Thursday
• Task 1
• Task 2

Friday
• Task 1
• Task 2

Saturday
• Mock test or practice task.

Sunday
• Revision and reflection.

## Subject Priorities
• Priority 1
• Priority 2
• Priority 3

## Weekly Goal
• One measurable goal for the end of the week.
"""

        response = get_llm().invoke(
            prompt
        )
        
        MemoryService.update_memory(
    student_id,
    {
        "last_study_plan": response.content,
        "weak_subject": summary.get("weakest_subject"),
        "academic_goal": profile.get("academic_goal")
    }
)
        return {

            "student_id": student_id,

            "study_plan": response.content,

            # Structured outputs
            "performance_summary": summary,

            "diagnostic_profile": profile,

            "student_memory": memory,

            "priority_subject": summary.get(
                "weakest_subject",
                ""
            ),

            "learning_style": profile.get(
                "learning_style",
                ""
            ),

            "academic_goal": profile.get(
                "academic_goal",
                ""
            )

        }