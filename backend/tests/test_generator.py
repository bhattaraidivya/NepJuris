from unittest.mock import MagicMock, patch

import pytest

from rag.generator import GenerationError, Generator


def _mock_response(status_code=200, json_data=None, text=""):
    resp = MagicMock()
    resp.status_code = status_code
    resp.json.return_value = json_data or {}
    resp.text = text
    return resp


GROQ_SUCCESS = _mock_response(200, {"choices": [{"message": {"content": "groq answer"}}]})
GEMINI_SUCCESS = _mock_response(200, {"candidates": [{"content": {"parts": [{"text": "gemini answer"}]}}]})
SERVER_ERROR = _mock_response(500, text="internal error")


@patch("rag.generator.GROQ_API_KEY", "fake-groq-key")
@patch("rag.generator.GEMINI_API_KEY", "fake-gemini-key")
class TestGeneratorFallback:
    @patch("rag.generator.requests.post", return_value=GROQ_SUCCESS)
    def test_uses_groq_when_it_succeeds(self, mock_post):
        result = Generator().generate("question", [])

        assert result == "groq answer"
        assert mock_post.call_count == 1  # Gemini never called

    @patch("rag.generator.requests.post", side_effect=[SERVER_ERROR, GEMINI_SUCCESS])
    def test_falls_back_to_gemini_when_groq_fails(self, mock_post):
        result = Generator().generate("question", [])

        assert result == "gemini answer"
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

    assert result == "gemini answer"
    assert mock_post.call_count == 1  # only Gemini was actually called over the network


@patch("rag.generator.GROQ_API_KEY", "")
@patch("rag.generator.GEMINI_API_KEY", "")
def test_raises_when_no_api_keys_configured():
    with pytest.raises(GenerationError):
        Generator().generate("question", [])
