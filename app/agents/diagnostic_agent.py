import json

from langchain_core.prompts import PromptTemplate

from app.utils.llm import get_llm
from app.services.memory_service import MemoryService
from app.services.diagnostic_service import DiagnosticService

class DiagnosticAgent:

    def __init__(self):

        self.llm = get_llm()

        with open(
            "app/prompts/diagnostic_prompt.txt",
            "r",
            encoding="utf-8"
        ) as f:
            self.prompt_template = f.read()

    def analyze(
        self,
        student_id,
        confidence_level,
        study_hours_per_day,
        academic_goal,
        preferred_learning_style,
        self_feedback
    ):

        prompt = PromptTemplate.from_template(
            self.prompt_template
        )

        final_prompt = prompt.format(
            confidence_level=confidence_level,
            study_hours_per_day=study_hours_per_day,
            academic_goal=academic_goal,
            preferred_learning_style=preferred_learning_style,
            self_feedback=self_feedback
        )

        response = self.llm.invoke(final_prompt)

        print("\nLLM RESPONSE:")
        print(response.content)

        try:

            cleaned_response = response.content.strip()

            cleaned_response = cleaned_response.replace(
                "```json",
                ""
            )

            cleaned_response = cleaned_response.replace(
                "```",
                ""
            )

            result = json.loads(cleaned_response)
            
            profile = {

    "student_id": student_id,

    "confidence_level": confidence_level,

    "study_hours_per_day": study_hours_per_day,

    "academic_goal": academic_goal,

    "preferred_learning_style": preferred_learning_style,

    "self_feedback": self_feedback,

    "strengths": result.get("strengths", []),

    "weaknesses": result.get("weaknesses", []),

    "learning_style": result.get("learning_style", ""),

    "risks": result.get("risks", [])

}
            DiagnosticService.save_profile(profile)

            # ------------------------------
            # Save important long-term memory
            # ------------------------------
            
            MemoryService.update_memory(
                student_id,
                {
                    "learning_style": result.get("learning_style", ""),
                    "strengths": result.get("strengths", []),
                    "weaknesses": result.get("weaknesses", []),
                    "academic_goal": academic_goal,
                    "confidence_level": confidence_level
                }
            )

            return result

        except Exception as e:

            print("\nJSON ERROR:")
            print(e)

        return {
            "strengths": [],
            "weaknesses": [],
            "learning_style": "Unknown",
            "risks": []
        }