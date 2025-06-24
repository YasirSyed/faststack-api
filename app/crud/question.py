from typing import Optional
from sqlalchemy.orm import Session
from app.models.question import Question
from app.models.tag import Tag
from app.schemas.question import QuestionCreate
from app.crud import tag as crud_tag

def get(db: Session, id: int) -> Optional[Question]:
    return db.query(Question).filter(Question.id == id).first()

def get_multi(db: Session, *, skip: int = 0, limit: int = 100):
    return db.query(Question).offset(skip).limit(limit).all()

def create(db: Session, *, obj_in: QuestionCreate, author_id: int) -> Question:
    # Create the question
    question = Question(
        title=obj_in.title,
        content=obj_in.content,
        author_id=author_id,
    )
    # Handle tags
    tags = []
    for tag_name in obj_in.tag_names or []:
        tag_obj = crud_tag.get_by_name(db, name=tag_name)
        if not tag_obj:
            tag_obj = Tag(name=tag_name)
            db.add(tag_obj)
            db.flush()  # Assigns an id
        tags.append(tag_obj)
    question.tags = tags
    db.add(question)
    db.commit()
    db.refresh(question)
    return question

 