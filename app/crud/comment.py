from typing import Optional
from sqlalchemy.orm import Session
from app.models.comment import Comment

def get(db: Session, id: int) -> Optional[Comment]:
    return db.query(Comment).filter(Comment.id == id).first()

def get_by_question(db: Session, question_id: int, *, skip: int = 0, limit: int = 100):
    return db.query(Comment).filter(Comment.question_id == question_id).offset(skip).limit(limit).all()

# Additional comment CRUD operations will be implemented here 