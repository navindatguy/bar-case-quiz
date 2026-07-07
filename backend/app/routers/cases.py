from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app import models, schemas

router = APIRouter(prefix="/cases", tags=["cases"])


@router.get("", response_model=list[schemas.CaseOut])
def list_cases(jurisdiction: str | None = None, limit: int = 50, db: Session = Depends(get_db)):
    query = db.query(models.Case)
    if jurisdiction:
        query = query.filter(models.Case.jurisdiction == jurisdiction)
    return query.limit(limit).all()


@router.get("/{case_id}", response_model=schemas.CaseDetailOut)
def get_case(case_id: int, db: Session = Depends(get_db)):
    case = db.query(models.Case).filter(models.Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return case
