from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import deps
from app.models.user import User

router = APIRouter()

@router.get("/users/me")
def read_current_user(
    current_user: User = Depends(deps.get_current_active_user),
):
    """Get current user."""
    return current_user

# Additional user endpoints will be implemented here 