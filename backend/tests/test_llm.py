"""M7 llm tests: JSON retry and provider fallback, no network."""
import json

import httpx
import openai
import pytest

from app import llm
from app.models import SentinelVerdict

GOOD = {"verdict": "scam", "confidence": 0.9, "matched_payment_entry_id": None,
        "red_flags": ["sender is not paypal.com"], "explanation": "No verified payment."}


def _reply(content: str) -> httpx.Response:
    return httpx.Response(200, json={
        "id": "x", "object": "chat.completion", "created": 0, "model": "m",
        "choices": [{"index": 0, "finish_reason": "stop", "message": {"role": "assistant", "content": content}}],
        "usage": {"prompt_tokens": 1, "completion_tokens": 1, "total_tokens": 2}})


def test_invalid_json_is_retried_once() -> None:
    replies = iter([_reply("not json"), _reply(json.dumps(GOOD))])
    client = httpx.Client(transport=httpx.MockTransport(lambda req: next(replies)))
    out = llm._call("groq", "m", "k", "sys", "user", SentinelVerdict, http_client=client)
    assert out.verdict == "scam"


def test_falls_back_to_next_provider(monkeypatch) -> None:
    from app.config import get_settings
    monkeypatch.setenv("LLM_PROVIDER", "groq")
    monkeypatch.setenv("LLM_FALLBACKS", "gemini:g,nvidia:m")
    monkeypatch.setenv("GROQ_API_KEY", "k")
    monkeypatch.setenv("NVIDIA_API_KEY", "k")
    monkeypatch.setenv("GEMINI_API_KEY", "")  # no key: skipped (env beats a real key in .env)
    get_settings.cache_clear()
    calls = []

    def fake_call(provider, model, key, system, user, schema):
        calls.append(provider)
        if provider == "groq":
            raise llm.LLMError("rate limited")
        return SentinelVerdict.model_validate(GOOD)

    monkeypatch.setattr(llm, "_call", fake_call)
    try:
        assert llm.complete("s", "u", SentinelVerdict).verdict == "scam"
        assert calls == ["groq", "nvidia"]
        monkeypatch.setattr(llm, "_call", lambda *a: (_ for _ in ()).throw(llm.LLMError("down")))
        with pytest.raises(llm.LLMError):
            llm.complete("s", "u", SentinelVerdict)
    finally:
        get_settings.cache_clear()
