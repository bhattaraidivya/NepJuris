import json
from unittest.mock import MagicMock, patch

import pytest

from rag.generator import GenerationError, Generator


def _mock_response(status_code=200, json_data=None):
    resp = MagicMock()
    resp.status_code = status_code
    resp.json.return_value = json_data or {}
    resp.text = json.dumps(json_data) if json_data else ""
    return resp


def _ollama_response(scope, answer):
    return _mock_response(200, {"response": json.dumps({"scope": scope, "answer": answer})})


@patch("rag.generator.requests.post", return_value=_ollama_response("in_scope", "the answer"))
def test_returns_answer_and_scope_on_success(mock_post):
    result = Generator().generate("question", [])

    assert result == {"answer": "the answer", "scope": "in_scope"}


@patch("rag.generator.requests.post", return_value=_ollama_response("out_of_scope", "not Nepal law"))
def test_tags_out_of_scope_answers(mock_post):
    result = Generator().generate("US helmet law", [])

    assert result == {"answer": "not Nepal law", "scope": "out_of_scope"}


@patch(
    "rag.generator.requests.post",
    return_value=_mock_response(200, {"response": "not json at all"}),
)
def test_falls_back_to_raw_text_when_response_is_not_json(mock_post):
    result = Generator().generate("question", [])

    assert result == {"answer": "not json at all", "scope": "in_scope"}


@patch(
    "rag.generator.requests.post",
    return_value=_mock_response(200, {"response": '```json\n{"scope": "greeting", "answer": "hi there"}\n```'}),
)
def test_strips_markdown_fences_around_json(mock_post):
    result = Generator().generate("hi", [])

    assert result == {"answer": "hi there", "scope": "greeting"}


@patch("rag.generator.requests.post", return_value=_mock_response(500))
def test_raises_on_non_200_status(mock_post):
    with pytest.raises(GenerationError):
        Generator().generate("question", [])


@patch("rag.generator.requests.post", return_value=_mock_response(200, {"unexpected": "shape"}))
def test_raises_on_unexpected_response_shape(mock_post):
    with pytest.raises(GenerationError):
        Generator().generate("question", [])
