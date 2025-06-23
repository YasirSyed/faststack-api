from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    pass

class CommentUpdate(BaseModel):
    content: Optional[str] = None

class CommentInDBBase(CommentBase):
    id: int
    author_id: int
    question_id: Optional[int] = None
    answer_id: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Comment(CommentInDBBase):
    author_username: Optional[str] = None 