from vs_qdrant import load_vector_store
from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq

load_dotenv()

print("Loading Vector Database...")
db = load_vector_store()
load_dotenv()

print("Connecting to Groq...")

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

print("\nSystem Ready!")
print("Type 'exit' to quit.\n")

while True:

    question = input("Ask Question: ")

    if question.lower() == "exit":
        print("Goodbye!")
        break

    print("\nRetrieving documents...\n")

    # -----------------------------
    # Retrieval with scores
    # -----------------------------
    results = db.similarity_search_with_score(
        question,
        k=5
    )

    print("=" * 80)
    print("SIMILARITY SCORES")
    print("=" * 80)

    for doc, score in results:

        print(
            f"{doc.metadata['subject']} -> "
            f"{doc.metadata['chapter']} -> "
            f"Page {doc.metadata.get('page', 'N/A')} -> "
            f"Score: {score:.4f}"
        )
        
    docs = [doc for doc, score in results]

    print("\n" + "=" * 80)
    print("RETRIEVED SOURCES")
    print("=" * 80)

    for doc in docs:

        print(
            f"{doc.metadata['subject']} -> "
            f"{doc.metadata['chapter']} -> "
            f"Page {doc.metadata.get('page', 'N/A')}"
        )

    print("\n" + "=" * 80)
    print("RETRIEVED CHUNKS")
    print("=" * 80)

    for i, doc in enumerate(docs, start=1):

        print(f"\nChunk {i}")
        print("-" * 40)

        print(doc.page_content[:500])

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    prompt = f"""
        You are an expert Class 11 teacher.

        Your task is to answer the student's question using ONLY the provided NCERT context.

        ==================================================

NCERT CONTEXT

{context}

==================================================

QUESTION

{question}

==================================================

INSTRUCTIONS

- Answer ONLY using the given NCERT context.
- Do NOT add information outside the context.
- Keep the explanation simple and easy to understand.
- Focus on exam-oriented understanding.
- Avoid repeating the same points.
- Use examples or analogies only if supported by the context.

IMPORTANT RESPONSE RULES

- Maximum 200 words.
- Use short headings.
- Use bullet points only.
- Do NOT write long paragraphs.
- Keep the answer concise and suitable for a web application.

OUTPUT FORMAT

## Simple Explanation
• Explain the concept in 2–3 bullets.

## NCERT Definition
• State the definition or principle.

## Key Points
• Mention 3–5 important facts.

## Common Mistakes
• Mention 2 common mistakes students make.

## Exam Tip
• Give one short exam-oriented tip.
"""

    print("\nGenerating Answer...\n")

    response = llm.invoke(prompt)

    print("=" * 80)
    print("ANSWER")
    print("=" * 80)

    print(response.content)

    print("\n" + "=" * 80 + "\n")