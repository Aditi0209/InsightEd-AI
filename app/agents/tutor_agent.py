from app.rag.vs_qdrant import load_vector_store
from app.utils.llm import get_llm
from app.services.memory_service import MemoryService


class TutorAgent:

    def __init__(self):

        self.db = load_vector_store()

    def answer_question(
        self,
        question: str,
        student_id: str
    ):

        # -------------------------------
        # Retrieve Relevant NCERT Context
        # -------------------------------
        results = self.db.similarity_search_with_score(
            question,
            k=5
        )

        docs = [
            doc
            for doc, score in results
        ]

        context = "\n\n".join(
            doc.page_content
            for doc in docs
        )

        # -------------------------------
        # Retrieve Student Memory
        # -------------------------------
        memory = MemoryService.get_memory(
            student_id
        )

        # -------------------------------
        # Tutor Prompt
        # -------------------------------
        prompt = f"""
You are an expert Class 11 academic tutor.

Your goal is to teach concepts clearly using ONLY the provided NCERT context.

Personalize the explanation using the student's previous learning history whenever relevant.

==================================================

STUDENT MEMORY

{memory}

==================================================

NCERT CONTEXT

{context}

==================================================

QUESTION

{question}

==================================================

INSTRUCTIONS

- Answer ONLY using the NCERT context.
- Do NOT invent information outside the provided context.
- Adapt the explanation according to the student's learning style if available.
- If previous weaknesses exist, relate your explanation to those areas.
- If previous misconceptions exist, correct them naturally.
- Keep the explanation simple, accurate, and exam-oriented.
- Focus on helping the student understand the concept quickly.
- Use examples or analogies only if they are supported by the NCERT context.
- Avoid unnecessary theory or repetition.

IMPORTANT RESPONSE RULES

- Maximum 250 words.
- Use short headings.
- Use bullet points only.
- Do NOT write long paragraphs.
- Keep each bullet concise.
- The response should be suitable for display inside a web application.

OUTPUT FORMAT

## Simple Explanation
• Explain the concept in 2–3 bullets.

## NCERT Definition
• Give the official definition or principle from the NCERT context.

## Key Points
• Mention the 3–5 most important facts.

## Common Mistakes
• List 2–3 mistakes students usually make.

## Exam Tip
• Give one practical exam-oriented tip.
"""

        response = get_llm().invoke(
            prompt
        )

        # -------------------------------
        # Sources
        # -------------------------------
        sources = []

        for doc in docs:

            sources.append(
                {
                    "subject": doc.metadata.get(
                        "subject"
                    ),
                    "chapter": doc.metadata.get(
                        "chapter"
                    )
                }
            )

        return {

            "student_id": student_id,

            "answer": response.content,

            "sources": sources

        }