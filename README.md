# InsightEd-AI

An AI-powered academic mentoring platform for school students. Students log in, add their test scores and a short diagnostic form, and get a RAG-based AI Tutor, performance insights, a personalized weekly study plan, and tailored feedback.

## Features

- **AI Tutor (RAG):** answers doubts from NCERT Class 11 content (Maths, Physics, Chemistry) retrieved from Qdrant, returning the subject and chapter as sources.
- **Performance analytics:** averages, strongest and weakest subjects and recent trends computed in Python; an LLM turns them into insights.
- **Study planner:** a rule-based base plan, personalized by the LLM using the student's profile and memory.
- **Diagnostic profiling:** a short form is analysed by the LLM into strengths, weaknesses, learning style and risks.
- **Feedback:** combines performance, profile and study plan into short, actionable feedback.
- **Supervisor routing:** an LLM-based supervisor reads the student's query and decides which agents to run.
- **Student memory:** a per-student MongoDB document stores the latest profile and summaries and personalizes prompts.
- **Authentication:** JWT-based register/login with bcrypt hashing; every endpoint uses the student ID from the token, so students can only access their own data.

## How It Works

**AI Tutor (RAG)**

```
Offline:  NCERT files ─► chunks (1000 chars, 200 overlap) ─► embeddings (all-MiniLM-L6-v2) ─► Qdrant
Online:   question ─► embed ─► top-5 similar chunks ─► prompt (+ student memory) ─► LLM ─► answer + sources
```

**Supervisor**

```
Student query ─► Supervisor (LLM picks agents) ─► Tutor / Performance / Planner / Feedback ─► combined response
```

Outputs are passed forward: the performance result feeds the planner, and both feed the feedback agent.

## Tech Stack

| Layer | Tools |
|---|---|
| Backend | FastAPI, Pydantic |
| Database | MongoDB (PyMongo) |
| Vector store | Qdrant |
| Embeddings | HuggingFace `sentence-transformers/all-MiniLM-L6-v2` |
| LLM framework | LangChain, Groq (`llama-3.3-70b-versatile`) |
| Auth | JWT (python-jose), bcrypt (passlib) |
| Frontend | React (runs on `localhost:5173`) |

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Create a `.env` file in the project root:
   ```
   MONGO_URI=your_mongodb_connection_string
   GROQ_API_KEY=your_groq_api_key
   QDRANT_URL=your_qdrant_url
   QDRANT_API_KEY=your_qdrant_api_key
   JWT_SECRET_KEY=your_long_random_secret
   JWT_ALGORITHM=HS256
   JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60
   ```
3. Place NCERT files (PDF, DOCX, TXT or MD) in `data/<subject>/`, then build the vector store once:
   ```bash
   cd app/rag
   python ingest.py
   ```
4. Start the API:
   ```bash
   uvicorn app.main:app --reload
   ```
5. Open the interactive docs at `http://127.0.0.1:8000/docs`.

## Design Decisions

- **Numbers are computed in code, not by the LLM:** averages and strongest/weakest subjects are deterministic. The LLM only explains them.
- **Student ID comes from the token, never from the request:** this prevents one student from reading another's data.
- **Grounded tutor answers:** the prompt restricts the Tutor to the retrieved NCERT context.
