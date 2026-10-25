import logging

import pytest

import tachyroute.engine as engine_module
from tachyroute import Router


def fake_pipeline(*args, **kwargs):
    def classify(text, candidate_labels, multi_label=False):
        return {"labels": list(candidate_labels), "scores": [0.95] + [0.01] * (len(candidate_labels) - 1)}

    return classify


@pytest.fixture(autouse=True)
def stub_pipeline(monkeypatch):
    monkeypatch.setattr(engine_module, "pipeline", fake_pipeline)


QUESTIONS = {
    "department": {
        "type": "choice",
        "instructions": "Which department?",
        "criteria": {"billing": "invoices", "technical": "bugs"},
    }
}


def test_package_logger_has_null_handler():
    handlers = logging.getLogger("tachyroute").handlers
    assert any(isinstance(h, logging.NullHandler) for h in handlers)


def test_predict_logs_info_and_debug(caplog):
    router = Router()
    with caplog.at_level(logging.DEBUG, logger="tachyroute"):
        router.predict("billed twice", QUESTIONS)

    records = [(r.name, r.levelno) for r in caplog.records]
    assert ("tachyroute.router", logging.INFO) in records
    assert ("tachyroute.engine", logging.INFO) in records
    assert ("tachyroute.router", logging.DEBUG) in records
    assert ("tachyroute.engine", logging.DEBUG) in records
    assert "Routing request to 'quantized-fast' model" in caplog.text


def test_debug_messages_hidden_at_info_level(caplog):
    router = Router()
    with caplog.at_level(logging.INFO, logger="tachyroute"):
        router.predict("billed twice", QUESTIONS)

    assert caplog.records
    assert all(r.levelno >= logging.INFO for r in caplog.records)


def test_nothing_printed_to_stdout(capsys):
    Router().predict("billed twice", QUESTIONS)
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""
