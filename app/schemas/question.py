from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel

class QuestionBase(BaseModel):
    title: str
    content: str

class QuestionCreate(QuestionBase):
    tag_names: Optional[List[str]] = []

class QuestionUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    tag_names: Optional[List[str]] = None

class QuestionInDBBase(QuestionBase):
    id: int
    author_id: int
    view_count: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Question(QuestionInDBBase):
    author_username: Optional[str] = None
    tags: Optional[List[str]] = []
    answer_count: Optional[int] = 0
    vote_count: Optional[int] = 0

class QuestionDetail(Question):
    answers: Optional[List["Answer"]] = []
    comments: Optional[List["Comment"]] = [] 