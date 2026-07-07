from unittest.mock import patch

from backend.app import models
from backend.app.services.question_generator import generate_questions_for_case

FAKE_LLM_RESPONSE = [
    {
        "prompt": "A police officer stops a car for a broken taillight. Under the "
        "rule from this case, may the officer search the trunk without a warrant?",
        "choice_a": "Yes, automatically, once any traffic stop is made.",
        "choice_b": "No, absent consent, a warrant, or an applicable exception.",
        "choice_c": "Yes, but only if the driver is arrested first.",
        "choice_d": "No, under no circumstances during a traffic stop.",
        "correct_choice": "B",
        "explanation": "The opinion holds that trunk searches require an exception "
        "to the warrant requirement; a broken taillight alone doesn't supply one.",
        "source_excerpt": "The court held that a routine traffic stop does not, by "
        "itself, justify a warrantless search of the vehicle's trunk.",
    }
]


def test_generate_questions_for_case_builds_question_objects():
    case = models.Case(
        id=1,
        cap_id="123",
        case_name="People v. Example",
        citation="123 Ill. 2d 456",
        court="Illinois Supreme Court",
        jurisdiction="Illinois",
        decision_date="2020-01-01",
        full_text="The court held that a routine traffic stop does not, by itself, "
        "justify a warrantless search of the vehicle's trunk.",
    )

    with patch(
        "backend.app.services.question_generator._call_claude",
        return_value=FAKE_LLM_RESPONSE,
    ):
        questions = generate_questions_for_case(case, topic="Motions to Suppress", count=1)

    assert len(questions) == 1
    q = questions[0]
    assert q.topic == "Motions to Suppress"
    assert q.correct_choice == "B"
    assert q.reviewed is False
    assert "warrantless" in q.source_excerpt
