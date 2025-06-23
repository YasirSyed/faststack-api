from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel
from app.schemas.comment import Comment

class AnswerBase(BaseModel):
    content: str

class AnswerCreate(AnswerBase):
    pass

class AnswerUpdate(BaseModel):
    content: Optional[str] = None

class AnswerInDBBase(AnswerBase):
    id: int
    question_id: int
    author_id: int
    is_accepted: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Answer(AnswerInDBBase):
    author_username: Optional[str] = None
    vote_count: Optional[int] = 0

class AnswerDetail(Answer):
    comments: Optional[List[Comment]] = [] 