from datetime import datetime

from sqlalchemy import String, Text, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.database import Base


class Case(Base):
 __tablename__ = "cases"

    id: Mapped[int] = mapped_column(primary_key=True)
    cap_id: Mapped[str] = mapped_column(String, unique=True, index=True)
    case_name: Mapped[str] = mapped_column(String)
    citation: Mapped[str] = mapped_column(String)
    court: Mapped[str] = mapped_column(String)
    jurisdiction: Mapped[str] = mapped_column(String)
    decision_date: Mapped[str] = mapped_column(String) 
    full_text: Mapped[str] = mapped_column(Text)
    source_url: Mapped[str] = mapped_column(String, nullable=True)
    questions: Mapped[list["Question"]] = relationship(back_populates="case")
class Question(Base):
 __tablename__ = "questions"

    id: Mapped[int] = mapped_column(primary_key=True)
    case_id: Mapped[int] = mapped_column(ForeignKey("cases.id"))
    topic: Mapped[str] = mapped_column(String, index=True)

    prompt: Mapped[str] = mapped_column(Text)
    choice_a: Mapped[str] = mapped_column(Text)
    choice_b: Mapped[str] = mapped_column(Text)
    choice_c: Mapped[str] = mapped_column(Text)
    choice_d: Mapped[str] = mapped_column(Text)
    correct_choice: Mapped[str] = mapped_column(String)  # abcd string
    explanation: Mapped[str] = mapped_column(Text)
    source_excerpt: Mapped[str] = mapped_column(Text)  # snippet of case text the answer relies on

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    case: Mapped["Case"] = relationship(back_populates="questions")
