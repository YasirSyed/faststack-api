from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import deps
from app.models.user import User

router = APIRouter()

@router.get("/tags")
def read_tags():
    """Get all tags."""
    return {"message": "Tags endpoint - to be implemented"}

# Additional tag endpoints will be implemented here 