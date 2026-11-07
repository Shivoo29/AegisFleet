"""LLM wrapper (M7). One complete() for every agent.

Providers are tried in order: LLM_PROVIDER:LLM_MODEL first, then each entry of
LLM_FALLBACKS. All real providers are reached through their OpenAI-compatible
endpoints, so one client covers Groq, Gemini and NVIDIA NIM.
"""
import json
import logging
import time
from pathlib import Path

import openai
from pydantic import BaseModel, ValidationError

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
FIXTURES = REPO_ROOT / "fixtures" / "llm"

BASE_URLS = {
    "groq": "https://api.groq.com/openai/v1",
    "gemini": "https://generativelanguage.googleapis.com/v1beta/openai/",
    "nvidia": "https://integrate.api.nvidia.com/v1",
}

log = logging.getLogger("aegis.llm")


class LLMError(Exception):
    pass


def complete(system: str, user: str, schema: type[BaseModel]) -> BaseModel:
    from app.config import get_settings
    s = get_settings()
    if s.llm_provider == "fake":
        return _fake(schema)
    chain = [(s.llm_provider, s.llm_model)] + s.llm_fallback_chain
    errors = []
    for provider, model in chain:
        key = getattr(s, f"{provider}_api_key", "")
        if not key:
            errors.append(f"{provider}: no API key")
            continue
        try:
            return _call(provider, model, key, system, user, schema)
        except (openai.APIError, LLMError) as e:  # rate limit, 5xx, timeout, or bad JSON twice
            log.warning("llm %s/%s failed: %s", provider, model, e)
            errors.append(f"{provider}/{model}: {e}")
    raise LLMError("all providers failed: " + " | ".join(errors))


def _call(provider: str, model: str, key: str, system: str, user: str, schema: type[BaseModel],
          http_client=None) -> BaseModel:
    # ponytail: json_object mode + schema in the prompt + Pydantic check works on all three
    # providers; switch a provider to strict json_schema if evals show invalid-JSON rates.
    client = openai.OpenAI(base_url=BASE_URLS[provider], api_key=key, timeout=30, max_retries=1,
                           http_client=http_client)
    messages = [
        {"role": "system", "content": f"{system}\n\nReply with one JSON object matching this JSON Schema, nothing else:\n"
                                      f"{json.dumps(schema.model_json_schema())}"},
        {"role": "user", "content": user},
    ]
    for attempt in (1, 2):
        t0 = time.monotonic()
        resp = client.chat.completions.create(model=model, messages=messages,
                                              response_format={"type": "json_object"})
        text = resp.choices[0].message.content or ""
        log.info("llm %s/%s %s attempt=%d tokens_in=%s tokens_out=%s latency_ms=%d", provider, model,
                 schema.__name__, attempt, getattr(resp.usage, "prompt_tokens", None),
                 getattr(resp.usage, "completion_tokens", None), (time.monotonic() - t0) * 1000)
        try:
            return schema.model_validate_json(text)
        except ValidationError as e:
            messages += [{"role": "assistant", "content": text},
                         {"role": "user", "content": f"That JSON was invalid: {e}. Reply with corrected JSON only."}]
    raise LLMError(f"invalid {schema.__name__} JSON after retry")


def _fake(schema: type[BaseModel]) -> BaseModel:
    path = FIXTURES / f"{schema.__name__}.json"
    try:
        return schema.model_validate_json(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise LLMError(f"no fixture for schema {schema.__name__}")
    except ValidationError as e:
        raise LLMError(f"bad fixture for {schema.__name__}: {e}")
