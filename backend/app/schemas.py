from pydantic import BaseModel


class CaseOut(BaseModel):
    id: int
    case_name: str
    citation: str
    court: str
    jurisdiction: str
    decision_date: str
    source_url: str | None = None

    class Config:
        from_attributes = True


class CaseDetailOut(CaseOut):
    full_text: str


class QuestionOut(BaseModel):
    id: int
    case_id: int
    topic: str
    prompt: str
    choice_a: str
    choice_b: str
    choice_c: str
    choice_d: str

    class Config:
        from_attributes = True


class QuestionAnswerOut(QuestionOut):
    """Returned only after the user submits an answer, or in review mode."""

    correct_choice: str
    explanation: str
    source_excerpt: str


class GenerateQuestionsRequest(BaseModel):
    case_id: int
    topic: str
    count: int = 3
