from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app import models, schemas
from backend.app.services.question_generator import generate_questions_for_case

router = APIRouter(prefix="/questions", tags=["questions"])


@router.get("", response_model=list[schemas.QuestionOut])
def list_questions(topic: str | None = None, limit: int = 20, db: Session = Depends(get_db)):
    query = db.query(models.Question).filter(models.Question.reviewed.is_(True))
    if topic:
        query = query.filter(models.Question.topic == topic)
    return query.limit(limit).all()


@router.get("/{question_id}/answer", response_model=schemas.QuestionAnswerOut)
def get_answer(question_id: int, db: Session = Depends(get_db)):
    """Reveal the correct answer, explanation, and source excerpt for a question."""
    question = db.query(models.Question).filter(models.Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question


@router.post("/generate", response_model=list[schemas.QuestionOut])
def generate_questions(req: schemas.GenerateQuestionsRequest, db: Session = Depends(get_db)):
    """Generate new questions for a case/topic pair using the LLM pipeline.

    Generated questions are saved with reviewed=False so they don't appear
    in the public quiz until a human has sanity-checked them.
    """
    case = db.query(models.Case).filter(models.Case.id == req.case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")

    new_questions = generate_questions_for_case(case, req.topic, req.count)
    db.add_all(new_questions)
    db.commit()
    for q in new_questions:
        db.refresh(q)
    return new_questions
