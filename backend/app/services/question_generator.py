"""
Generates bar-exam-style multiple-choice questions from a case opinion using
the Anthropic API.

Important: generated questions are saved with reviewed=False. A human should
spot-check each batch before it's exposed to real users via the /questions
list endpoint (which filters on reviewed=True) — an LLM can misstate a
holding or invent a plausible-sounding but wrong rule, and that's a bad
thing to hand someone studying for the actual bar.
"""

import argparse
import json

import anthropic

from backend.app.config import settings
from backend.app import models
from backend.app.database import SessionLocal

MODEL = "claude-sonnet-4-6"

SYSTEM_PROMPT = """You write bar-exam-style multiple choice questions based on real \
court opinions. Given a case opinion and a legal topic, write questions that test \
whether a reader understands the rule the case applies or establishes -- not just \
trivia about case names or dates.

Respond ONLY with a JSON array, no other text, matching this schema:

[
  {
    "prompt": "fact-pattern-based question text",
    "choice_a": "...",
    "choice_b": "...",
    "choice_c": "...",
    "choice_d": "...",
    "correct_choice": "A" | "B" | "C" | "D",
    "explanation": "why the correct choice is right and the others are wrong",
    "source_excerpt": "short excerpt (1-3 sentences) from the opinion that supports the answer"
  }
]
"""


def _build_user_prompt(case_text: str, topic: str, count: int) -> str:
    # Truncate very long opinions to keep requests reasonably sized; most
    # opinions relevant to a single doctrinal point don't need the full text.
    excerpt = case_text[:12000]
    return (
        f"Topic: {topic}\n\n"
        f"Case opinion text:\n{excerpt}\n\n"
        f"Write {count} multiple-choice bar-exam-style questions testing this topic "
        f"as applied in this case."
    )


def _call_claude(case_text: str, topic: str, count: int) -> list[dict]:
    client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

    response = client.messages.create(
        model=MODEL,
        max_tokens=4000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": _build_user_prompt(case_text, topic, count)}],
    )

    text = "".join(block.text for block in response.content if block.type == "text")
    text = text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    return json.loads(text)


def generate_questions_for_case(case: models.Case, topic: str, count: int) -> list[models.Question]:
    raw_questions = _call_claude(case.full_text, topic, count)

    questions = []
    for q in raw_questions:
        questions.append(
            models.Question(
                case_id=case.id,
                topic=topic,
                prompt=q["prompt"],
                choice_a=q["choice_a"],
                choice_b=q["choice_b"],
                choice_c=q["choice_c"],
                choice_d=q["choice_d"],
                correct_choice=q["correct_choice"],
                explanation=q["explanation"],
                source_excerpt=q["source_excerpt"],
                reviewed=False,
            )
        )
    return questions


def _cli():
    parser = argparse.ArgumentParser(description="Generate questions for a case already in the DB.")
    parser.add_argument("--case-id", type=int, required=True)
    parser.add_argument("--topic", type=str, required=True)
    parser.add_argument("--count", type=int, default=3)
    args = parser.parse_args()

    db = SessionLocal()
    try:
        case = db.query(models.Case).filter(models.Case.id == args.case_id).first()
        if not case:
            print(f"No case with id {args.case_id}")
            return
        questions = generate_questions_for_case(case, args.topic, args.count)
        db.add_all(questions)
        db.commit()
        print(f"Generated {len(questions)} questions for case {case.case_name!r}")
    finally:
        db.close()


if __name__ == "__main__":
    _cli()
