from app.services.analytics_service import AnalyticsService
from app.services.diagnostic_service import DiagnosticService
from app.services.memory_service import MemoryService
from app.utils.llm import get_llm


class PerformanceAgent:

    def generate_report(
        self,
        student_id: str
    ):

        # ---------------------------------------
        # Performance Summary
        # ---------------------------------------

        summary = AnalyticsService.generate_performance_summary(
            student_id
        )

        if "message" in summary:
            return summary

        # ---------------------------------------
        # Diagnostic Profile
        # ---------------------------------------

        profile = DiagnosticService.get_profile(
            student_id
        )

        if not profile:

            profile = {
                "strengths": [],
                "weaknesses": [],
                "learning_style": "Unknown",
                "academic_goal": "General Improvement",
                "risks": []
            }

        # ---------------------------------------
        # Student Memory
        # ---------------------------------------

        memory = MemoryService.get_memory(
            student_id
        )

        # ---------------------------------------
        # Prompt
        # ---------------------------------------

        prompt = f"""
You are an expert academic performance mentor.

Analyze the student's academic progress using:

- Historical performance
- Diagnostic profile
- Long-term student memory

Generate personalized insights based only on the provided information.

==================================================

STUDENT MEMORY

{memory}

==================================================

PERFORMANCE SUMMARY

Average Score:
{summary["average_score"]}

Strongest Subject:
{summary["strongest_subject"]}

Weakest Subject:
{summary["weakest_subject"]}

Subject Averages:
{summary["subject_averages"]}

Recent Performance:
{summary.get("recent_performance", [])}

==================================================

DIAGNOSTIC PROFILE

Strengths:
{profile.get("strengths", [])}

Weaknesses:
{profile.get("weaknesses", [])}

Learning Style:
{profile.get("learning_style", "")}

Academic Goal:
{profile.get("academic_goal", "")}

Risks:
{profile.get("risks", [])}

==================================================

INSTRUCTIONS

- Analyze the student's overall academic progress.
- Explain why the weakest subject is still weak.
- Highlight the strongest subject and how it can help improve weaker subjects.
- Compare current performance with previous trends if memory contains historical information.
- Identify recurring mistakes or learning patterns.
- Connect observations with the student's learning style.
- Consider the student's academic goal while giving recommendations.
- Suggest only practical next steps.
- Reuse previous successful learning strategies if available.
- Avoid generic observations.
- Do NOT repeat raw statistics already shown above.

IMPORTANT RESPONSE RULES

- Maximum 250 words.
- Use short headings.
- Use bullet points only.
- Do NOT write long paragraphs.
- Each bullet should be one concise sentence.
- Maximum 3 bullets under each section.
- Keep the response suitable for display inside a web application.
- Focus on insights rather than describing every statistic.

OUTPUT FORMAT

## Overall Progress
• Overall academic status.
• Biggest positive trend.

## Strengths
• Top strengths.
• How they can be leveraged.

## Areas Needing Attention
• Biggest weakness.
• Possible reason.

## Recommended Next Steps
• Top 3 practical actions.

## Outlook
• One short concluding observation about future improvement.
"""

        response = get_llm().invoke(
            prompt
        )

        # ---------------------------------------
        # Save Summary into Memory
        # ---------------------------------------
        
        MemoryService.update_memory(
            student_id,
            {
                "last_average_score": summary["average_score"],
                "last_weak_subject": summary["weakest_subject"],
                "last_strong_subject": summary["strongest_subject"],
                "last_performance_summary": summary,
                "last_performance_analysis": response.content
            }
        )

        return {

            "student_id": student_id,

            "analysis": response.content,

            "performance_summary": summary,

            "diagnostic_profile": profile,

            "student_memory": memory

        }