from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.question import Question, QuestionCreate, QuestionDetail
from app.crud import question as crud_question
from app.schemas.answer import Answer

router = APIRouter()

@router.get("/questions", response_model=list[Question])
def get_questions(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(deps.get_db),
):
    """Get all questions."""
    questions = crud_question.get_multi(db, skip=skip, limit=limit)
    result = []
    for q in questions:
        q_dict = {**q.__dict__}
        # Remove SQLAlchemy state
        q_dict.pop('_sa_instance_state', None)
        # Replace tags with tag names
        q_dict['tags'] = [t.name for t in q.tags]
        q_dict['author_username'] = q.author.username if q.author else None
        q_dict['answer_count'] = len(q.answers) if hasattr(q, 'answers') and q.answers is not None else 0
        # Calculate vote count
        q_dict['vote_count'] = sum(1 if v.vote_type.value == 'up' else -1 for v in q.votes) if hasattr(q, 'votes') and q.votes is not None else 0
        result.append(Question(**q_dict))
    return result

@router.get("/questions/{question_id}", response_model=QuestionDetail)
def get_question(
    question_id: int,
    db: Session = Depends(deps.get_db),
):
    """Get a single question by ID."""
    q = crud_question.get(db, id=question_id)
    if not q:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Question not found")
    q_dict = {**q.__dict__}
    q_dict.pop('_sa_instance_state', None)
    q_dict['tags'] = [t.name for t in q.tags]
    q_dict['author_username'] = q.author.username if q.author else None
    q_dict['answer_count'] = len(q.answers) if hasattr(q, 'answers') and q.answers is not None else 0
    q_dict['vote_count'] = sum(1 if v.vote_type.value == 'up' else -1 for v in q.votes) if hasattr(q, 'votes') and q.votes is not None else 0

    # Prepare answers: accepted first, then by vote count desc, then by updated_at desc
    def answer_sort_key(ans):
        return (
            0 if ans.is_accepted else 1,  # accepted first
            -sum(1 if v.vote_type.value == 'up' else -1 for v in ans.votes),  # vote count desc
            -ans.updated_at.timestamp() if ans.updated_at else 0  # updated_at desc
        )
    ordered_answers = sorted(q.answers, key=answer_sort_key)
    answer_objs = []
    for a in ordered_answers:
        a_dict = {**a.__dict__}
        a_dict.pop('_sa_instance_state', None)
        a_dict['author_username'] = a.author.username if a.author else None
        a_dict['vote_count'] = sum(1 if v.vote_type.value == 'up' else -1 for v in a.votes)
        answer_objs.append(Answer(**a_dict))
    q_dict['answers'] = answer_objs
    return QuestionDetail(**q_dict)


# Additional question endpoints will be implemented here 