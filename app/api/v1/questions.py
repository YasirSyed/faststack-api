from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import deps
from app.models.user import User

router = APIRouter()

@router.get("/questions")
def read_questions():
    """Get all questions."""
    return {"message": "Questions endpoint - to be implemented"}

# Additional question endpoints will be implemented here 