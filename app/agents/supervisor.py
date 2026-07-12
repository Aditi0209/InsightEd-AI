from app.utils.llm import get_llm

from app.agents.tutor_agent import TutorAgent
from app.agents.performance_agent import PerformanceAgent
from app.agents.planner_agent import PlannerAgent
from app.agents.feedback_agent import FeedbackAgent
from app.services.memory_service import MemoryService

from app.services.student_service import StudentService
from app.services.performance_service import PerformanceService


class SupervisorAgent:

    def __init__(self):

        self.tutor_agent = TutorAgent()
        self.performance_agent = PerformanceAgent()
        self.planner_agent = PlannerAgent()
        self.feedback_agent = FeedbackAgent()

    def _load_student_context(self, student_id: str):

        student = StudentService.get_student(student_id)

        performance = PerformanceService.get_student_tests(student_id)

        memory = MemoryService.get_memory(
            student_id
        )
 
        return {

            "student": student,

            "performance": performance,

            "memory": memory 

        }

    def route_query(
        self,
        query: str,
        student_id: str
    ):

        router_prompt = f"""
You are the Supervisor Agent of an Academic Mentor AI.

Your ONLY job is to decide which specialized agents should execute for the user's request.

Do NOT answer the user's question.
Do NOT explain your reasoning.
Return ONLY the required agent names.

==================================================

AVAILABLE AGENTS

TUTOR
- Answer academic questions.
- Explain concepts using NCERT knowledge.
- Solve subject-related doubts.

PERFORMANCE
- Analyze academic performance.
- Identify strengths and weaknesses.
- Analyze test history and progress.

PLANNER
- Generate personalized weekly study plans.
- Prioritize weak subjects.
- Recommend study strategies.

FEEDBACK
- Generate personalized motivational and improvement feedback.
- Review performance and study plan.
- Suggest practical improvements.

==================================================

ROUTING RULES

1. Execute ONLY the agents required.

2. If the user asks an academic question,
return:
TUTOR

3. If the user asks about performance,
return:
PERFORMANCE

4. If the user asks for a study plan,
return:
PERFORMANCE
PLANNER

5. If the user asks how to improve,
return:
PERFORMANCE
PLANNER
FEEDBACK

6. If the user asks for motivation or overall advice,
return:
PERFORMANCE
FEEDBACK

7. If the user asks an academic doubt AND also requests a study plan,
return:
TUTOR
PERFORMANCE
PLANNER

8. If the user asks an academic doubt AND also asks how to improve,
return:
TUTOR
PERFORMANCE
PLANNER
FEEDBACK

==================================================

IMPORTANT

- Return ONLY agent names.
- One agent per line.
- No numbering.
- No explanations.
- No extra text.
- No markdown.

==================================================

EXAMPLES

Question:
Explain Newton's Laws.

Output:
TUTOR

Question:
Analyze my academic performance.

Output:
PERFORMANCE

Question:
Create a study plan.

Output:
PERFORMANCE
PLANNER

Question:
How can I improve my Chemistry score?

Output:
PERFORMANCE
PLANNER
FEEDBACK

Question:
Explain Gravitation and create a study plan.

Output:
TUTOR
PERFORMANCE
PLANNER

Question:
Explain Organic Chemistry and tell me how I can improve.

Output:
TUTOR
PERFORMANCE
PLANNER
FEEDBACK

==================================================

User Query:
{query}
"""

        decision = (
            get_llm()
            .invoke(router_prompt)
            .content
            .strip()
        )

        workflow = [
            agent.strip().upper()
            for agent in decision.splitlines()
            if agent.strip()
        ]

        print("\n==============================")
        print("Workflow Selected")
        print(workflow)
        print("==============================\n")

        student_context = self._load_student_context(
            student_id
        )

        tutor_result = None
        performance_result = None
        planner_result = None
        feedback_result = None

        for agent in workflow:

            if agent == "TUTOR":

                tutor_result = self.tutor_agent.answer_question(query,student_id)

            elif agent == "PERFORMANCE":

                performance_result = (
                    self.performance_agent.generate_report(
                        student_id
                    )
                )

            elif agent == "PLANNER":

                planner_result = (
                    self.planner_agent.generate_personalized_plan(
                        student_id,
                        performance_result
                    )
                )

            elif agent == "FEEDBACK":

                feedback_result = (
                    self.feedback_agent.generate_feedback(
                        student_id,
                        performance_result,
                        planner_result
                    )
                )

        return {

            "workflow": workflow,

            "student_context": student_context,

            "tutor": tutor_result,

            "performance": performance_result,

            "planner": planner_result,

            "feedback": feedback_result

        }