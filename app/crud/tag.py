from typing import Optional
from sqlalchemy.orm import Session
from app.models.tag import Tag

def get(db: Session, id: int) -> Optional[Tag]:
    return db.query(Tag).filter(Tag.id == id).first()

def get_by_name(db: Session, *, name: str) -> Optional[Tag]:
    return db.query(Tag).filter(Tag.name == name).first()

def get_multi(db: Session, *, skip: int = 0, limit: int = 100):
    return db.query(Tag).offset(skip).limit(limit).all()

# Additional tag CRUD operations will be implemented here 