from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import deps
from app.models.user import User

router = APIRouter()

@router.get("/questions/{question_id}/comments")
def read_question_comments(question_id: int):
    """Get comments for a question."""
    return {"message": f"Comments for question {question_id} - to be implemented"}

# Additional comment endpoints will be implemented here 