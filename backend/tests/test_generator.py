import json
from unittest.mock import MagicMock, patch

import pytest

from rag.generator import GenerationError, Generator


def _mock_response(status_code=200, json_data=None, text=""):
    resp = MagicMock()
    resp.status_code = status_code
    resp.json.return_value = json_data or {}
    resp.text = text
    return resp


def _json_content(scope, answer):
    return json.dumps({"scope": scope, "answer": answer})


GROQ_SUCCESS = _mock_response(
    200, {"choices": [{"message": {"content": _json_content("in_scope", "groq answer")}}]}
)
GEMINI_SUCCESS = _mock_response(
    200, {"candidates": [{"content": {"parts": [{"text": _json_content("in_scope", "gemini answer")}]}}]}
)
SERVER_ERROR = _mock_response(500, text="internal error")


@patch("rag.generator.GROQ_API_KEY", "fake-groq-key")
@patch("rag.generator.GEMINI_API_KEY", "fake-gemini-key")
class TestGeneratorFallback:
    @patch("rag.generator.requests.post", return_value=GROQ_SUCCESS)
    def test_uses_groq_when_it_succeeds(self, mock_post):
        result = Generator().generate("question", [])

        assert result == {"answer": "groq answer", "scope": "in_scope"}
        assert mock_post.call_count == 1  # Gemini never called

    @patch("rag.generator.requests.post", side_effect=[SERVER_ERROR, GEMINI_SUCCESS])
    def test_falls_back_to_gemini_when_groq_fails(self, mock_post):
        result = Generator().generate("question", [])

        assert result == {"answer": "gemini answer", "scope": "in_scope"}
        assert mock_post.call_count == 2

    @patch("rag.generator.requests.post", return_value=SERVER_ERROR)
    def test_raises_when_both_backends_fail(self, mock_post):
        with pytest.raises(GenerationError):
            Generator().generate("question", [])


@patch("rag.generator.GEMINI_API_KEY", "fake-gemini-key")
@patch("rag.generator.GROQ_API_KEY", "")
@patch("rag.generator.requests.post", return_value=GEMINI_SUCCESS)
def test_skips_groq_and_uses_gemini_when_groq_key_missing(mock_post):
    result = Generator().generate("question", [])

    assert result == {"answer": "gemini answer", "scope": "in_scope"}
    assert mock_post.call_count == 1  # only Gemini was actually called over the network


@patch("rag.generator.GROQ_API_KEY", "")
@patch("rag.generator.GEMINI_API_KEY", "")
def test_raises_when_no_api_keys_configured():
    with pytest.raises(GenerationError):
        Generator().generate("question", [])


@patch("rag.generator.GROQ_API_KEY", "fake-groq-key")
@patch("rag.generator.GEMINI_API_KEY", "")
class TestScopeClassification:
    @patch(
        "rag.generator.requests.post",
        return_value=_mock_response(
            200, {"choices": [{"message": {"content": _json_content("out_of_scope", "not Nepal law")}}]}
        ),
    )
    def test_tags_out_of_scope_answers(self, mock_post):
        result = Generator().generate("US helmet law", [])

        assert result == {"answer": "not Nepal law", "scope": "out_of_scope"}

    @patch(
        "rag.generator.requests.post",
        return_value=_mock_response(200, {"choices": [{"message": {"content": "not json at all"}}]}),
    )
    def test_falls_back_to_raw_text_when_response_is_not_json(self, mock_post):
        result = Generator().generate("question", [])

        assert result == {"answer": "not json at all", "scope": "in_scope"}

    @patch(
        "rag.generator.requests.post",
        return_value=_mock_response(
            200,
            {
                "choices": [
                    {"message": {"content": '```json\n{"scope": "greeting", "answer": "hi there"}\n```'}}
                ]
            },
        ),
    )
    def test_strips_markdown_fences_around_json(self, mock_post):
        result = Generator().generate("hi", [])

        assert result == {"answer": "hi there", "scope": "greeting"}


@patch("rag.generator.GROQ_API_KEY", "fake-groq-key")
@patch("rag.generator.GEMINI_API_KEY", "")
class TestConversationHistory:
    @patch("rag.generator.requests.post", return_value=GROQ_SUCCESS)
    def test_history_turns_are_forwarded_to_groq_as_messages(self, mock_post):
        history = [
            {"role": "user", "content": "what is the divorce law"},
            {"role": "assistant", "content": "here's what applies..."},
        ]

        Generator().generate("what about for married couples?", [], history)

        sent_messages = mock_post.call_args.kwargs["json"]["messages"]
        assert sent_messages[0]["role"] == "system"
        assert sent_messages[1] == {"role": "user", "content": "what is the divorce law"}
        assert sent_messages[2] == {"role": "assistant", "content": "here's what applies..."}
        assert sent_messages[-1]["role"] == "user"

    @patch("rag.generator.requests.post", return_value=GROQ_SUCCESS)
    def test_history_is_truncated_to_max_messages(self, mock_post):
        history = [{"role": "user", "content": f"turn {i}"} for i in range(20)]

        Generator().generate("latest question", [], history)

        sent_messages = mock_post.call_args.kwargs["json"]["messages"]
        # system + MAX_HISTORY_MESSAGES + final user turn
        from rag.generator import MAX_HISTORY_MESSAGES

        assert len(sent_messages) == 1 + MAX_HISTORY_MESSAGES + 1
        assert sent_messages[1]["content"] == "turn 14"  # oldest kept turn
