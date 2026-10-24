import json
from fastapi import FastAPI, HTTPException
app = FastAPI(title="InterviewIQ Backend")
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from database import create_table,save_interview,get_history

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500"
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"]
)
create_table()


questions = {
    "python": [
        "What is Python, and what is it used for?",
        "What is the difference between a list and a tuple?",
        "What is a function in Python?"
    ],
    "java": [
        "What is Java?",
        "What is the difference between a class and an object?",
        "What is inheritance in Java?"
    ],
    "web": [
        "What is HTML?",
        "What is the difference between CSS and JavaScript?",
        "What is the purpose of an API?"
    ]
}


@app.get("/")
def home():
    return {"message": "Welcome to InterviewIQ Backend!"}


@app.get("/question")
def get_question(role: str = "python"):
    role = role.lower()

    if role not in questions:
        raise HTTPException(
            status_code=404,
            detail="Role not found. Choose python, java, or web."
        )

    return {
        "role": role,
        "questions": questions[role]
    }


class AnswerRequest(BaseModel):
    role: str
    question: str
    answer: str


@app.post("/answer")
def submit_answer(data: AnswerRequest):
    if not data.answer.strip():
        raise HTTPException(
            status_code=400,
            detail="Answer cannot be empty."
        )

    return {
        "message": "Answer received successfully!",
        "role": data.role,
        "question": data.question,
        "answer": data.answer
    }
class FeedbackRequest(BaseModel):
    role: str
    question: str
    answer: str


@app.post("/feedback")
def get_feedback(data: FeedbackRequest):
    answer = data.answer.strip()

    if not answer:
        raise HTTPException(
            status_code=400,
            detail="Answer cannot be empty."
        )

    word_count = len(answer.split())

    feedback = {
        "relevance": (
            "Review whether the answer addresses the question."
            if word_count < 8
            else "The answer contains relevant detail; verify its accuracy."
        ),
        "structure": (
            "Try organizing your answer into clear steps."
            if word_count < 15
            else "Try organizing your answer into clear points."
        ),
        "evidence": (
            "Add a practical example to support your answer."
            if word_count < 25
            else "Consider including a specific example."
        ),
        "role_knowledge": (
            f"Check that the answer demonstrates knowledge relevant to {data.role}."
        ),
        "clarity": (
            "Expand your answer using complete sentences."
            if word_count < 8
            else "Review your wording to ensure each point is clear."
        )
    }

    save_interview(
        data.role,
        data.question,
        answer,
        json.dumps(feedback)
    )

    return {
        "message": "Feedback generated and saved successfully!",
        "role": data.role,
        "question": data.question,
        "answer": answer,
        "word_count": word_count,
        "feedback": feedback,
        "note": "Basic rule-based feedback, not AI evaluation."
    }

@app.get("/history")
def interview_history():
    return{
        "history":get_history()
    }


@app.get("/health")
def health_check():
    return{
        "status":"healthy",
        "project":"InterviewIQ Backend"
    }
