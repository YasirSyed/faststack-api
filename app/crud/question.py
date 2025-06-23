from typing import Optional
from sqlalchemy.orm import Session
from app.models.question import Question

def get(db: Session, id: int) -> Optional[Question]:
    return db.query(Question).filter(Question.id == id).first()

def get_multi(db: Session, *, skip: int = 0, limit: int = 100):
    return db.query(Question).offset(skip).limit(limit).all()

 