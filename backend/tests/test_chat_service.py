from unittest.mock import MagicMock

from services.chat_service import ChatService

CONTEXTS = [{"source": "Civil Code", "page": 1, "section": None, "article": None}]


def _service_with(scope):
    service = ChatService.__new__(ChatService)  # skip __init__, avoid loading real retriever/generator
    service.retriever = MagicMock()
    service.retriever.retrieve.return_value = CONTEXTS
    service.generator = MagicMock()
    service.generator.generate.return_value = {"answer": "the answer", "scope": scope}
    return service


def test_in_scope_answer_includes_sources():
    result = _service_with("in_scope").generate_response("question")

    assert result["response"] == "the answer"
    assert result["sources"] == [{"source": "Civil Code", "page": 1, "section": None, "article": None}]


def test_out_of_scope_answer_has_no_sources():
    result = _service_with("out_of_scope").generate_response("US helmet law")

    assert result["response"] == "the answer"
    assert result["sources"] == []


def test_greeting_has_no_sources():
    result = _service_with("greeting").generate_response("hi")

    assert result["sources"] == []
