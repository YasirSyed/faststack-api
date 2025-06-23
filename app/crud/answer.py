from typing import Optional
from sqlalchemy.orm import Session
from app.models.answer import Answer

def get(db: Session, id: int) -> Optional[Answer]:
    return db.query(Answer).filter(Answer.id == id).first()

def get_by_question(db: Session, question_id: int, *, skip: int = 0, limit: int = 100):
    return db.query(Answer).filter(Answer.question_id == question_id).offset(skip).limit(limit).all()

# Additional answer CRUD operations will be implemented here 