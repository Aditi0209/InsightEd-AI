from fastapi import FastAPI

from app.api.chat import router as chat_router
from app.api.student import router as student_router
from app.api.performance import router as performance_router
from app.api.planner import router as planner_router
from app.api.diagnostic import router as diagnostic_router
from app.api.test import router as test_router
from app.api.feedback import router as feedback_router
from app.api.auth import router as auth_router
app = FastAPI(
    title="Academic Mentor AI"
)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(student_router)
app.include_router(performance_router)
app.include_router(planner_router)
app.include_router(diagnostic_router)
app.include_router(test_router)
app.include_router(feedback_router)

@app.get("/")
def root():

    return {
        "message": "Academic Mentor AI Running"
    }
    