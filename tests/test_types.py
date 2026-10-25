import pytest
from pydantic import ValidationError

from tachyroute.types import ChoiceQuestion, DecisionResult, ScoreQuestion


# ChoiceQuestion

def test_choice_question_valid():
    q = ChoiceQuestion(
        instructions="Pick the sentiment",
        criteria={"positive": "Happy tone", "negative": "Unhappy tone"},
    )
    assert q.instructions == "Pick the sentiment"
    assert q.criteria == {"positive": "Happy tone", "negative": "Unhappy tone"}


def test_choice_question_default_type():
    q = ChoiceQuestion(instructions="Pick one", criteria={"a": "first"})
    assert q.type == "choice"


def test_choice_question_requires_instructions():
    with pytest.raises(ValidationError, match="instructions"):
        ChoiceQuestion(criteria={"a": "first"})


def test_choice_question_requires_criteria():
    with pytest.raises(ValidationError, match="criteria"):
        ChoiceQuestion(instructions="Pick one")


def test_choice_question_criteria_must_be_dict():
    with pytest.raises(ValidationError, match="criteria"):
        ChoiceQuestion(instructions="Pick one", criteria=["a", "b"])


def test_choice_question_criteria_values_must_be_strings():
    with pytest.raises(ValidationError, match="criteria"):
        ChoiceQuestion(instructions="Pick one", criteria={"a": ["not", "a", "string"]})


# ScoreQuestion

def test_score_question_valid():
    q = ScoreQuestion(
        instructions="Rate the answer",
        criteria=["accuracy", "clarity"],
    )
    assert q.instructions == "Rate the answer"
    assert q.criteria == ["accuracy", "clarity"]


def test_score_question_default_type():
    q = ScoreQuestion(instructions="Rate it", criteria=["accuracy"])
    assert q.type == "score"


def test_score_question_requires_instructions():
    with pytest.raises(ValidationError, match="instructions"):
        ScoreQuestion(criteria=["accuracy"])


def test_score_question_requires_criteria():
    with pytest.raises(ValidationError, match="criteria"):
        ScoreQuestion(instructions="Rate it")


def test_score_question_criteria_must_be_list():
    with pytest.raises(ValidationError, match="criteria"):
        ScoreQuestion(instructions="Rate it", criteria={"accuracy": "how correct"})


def test_score_question_criteria_items_must_be_strings():
    with pytest.raises(ValidationError, match="criteria"):
        ScoreQuestion(instructions="Rate it", criteria=[1, 2])


# DecisionResult

def test_decision_result_valid():
    r = DecisionResult(
        answer="positive",
        confidence=0.93,
        evidence=["great product"],
        exit_layer=4,
    )
    assert r.answer == "positive"
    assert r.confidence == 0.93
    assert r.evidence == ["great product"]
    assert r.exit_layer == 4


def test_decision_result_optional_fields_default_to_none():
    r = DecisionResult(answer="yes", confidence=0.5)
    assert r.evidence is None
    assert r.exit_layer is None


def test_decision_result_answer_accepts_any_type():
    assert DecisionResult(answer=3, confidence=0.1).answer == 3
    assert DecisionResult(answer={"a": 1}, confidence=0.1).answer == {"a": 1}
    assert DecisionResult(answer=None, confidence=0.1).answer is None


def test_decision_result_requires_answer():
    with pytest.raises(ValidationError, match="answer"):
        DecisionResult(confidence=0.5)


def test_decision_result_requires_confidence():
    with pytest.raises(ValidationError, match="confidence"):
        DecisionResult(answer="yes")


def test_decision_result_confidence_must_be_numeric():
    with pytest.raises(ValidationError, match="confidence"):
        DecisionResult(answer="yes", confidence="very sure")


def test_decision_result_confidence_coerces_int_to_float():
    r = DecisionResult(answer="yes", confidence=1)
    assert r.confidence == 1.0
    assert isinstance(r.confidence, float)


def test_decision_result_evidence_must_be_list_of_strings():
    with pytest.raises(ValidationError, match="evidence"):
        DecisionResult(answer="yes", confidence=0.5, evidence="not a list")


def test_decision_result_exit_layer_must_be_integer():
    with pytest.raises(ValidationError, match="exit_layer"):
        DecisionResult(answer="yes", confidence=0.5, exit_layer="early")
