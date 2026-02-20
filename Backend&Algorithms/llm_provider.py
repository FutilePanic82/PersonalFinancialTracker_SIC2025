"""
llm_provider.py — LLM abstraction layer.
==========================================================
Reads configuration from the project-root `.env` and exposes a single
function ``llm_chat(messages) -> str`` that works transparently with
Ollama (local GPU), OpenAI, or Groq.

Supported LLM_MODE values:  ollama | openai | groq
"""
from __future__ import annotations

import logging
import os
import re

from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# ── Load .env from the project root ────────────────────────────────────────────
_ROOT = os.path.dirname(os.path.dirname(__file__))
_ENV_PATH = os.path.join(_ROOT, ".env")
load_dotenv(_ENV_PATH)

LLM_MODE = os.getenv("LLM_MODE", "ollama").lower()
LLM_MODEL = os.getenv("LLM_MODEL", "")

# ── Provider-specific defaults ─────────────────────────────────────────────────
_DEFAULT_MODELS = {
    "ollama": "llama3.2:3b",
    "openai": "gpt-4o-mini",
    "groq": "llama-3.1-8b-instant",
}

if not LLM_MODEL:
    LLM_MODEL = _DEFAULT_MODELS.get(LLM_MODE, "llama3.2:3b")

logger.info("LLM provider: %s  |  model: %s", LLM_MODE, LLM_MODEL)


# ── Strip <think> tags helper ──────────────────────────────────────────────────
def _strip_think(text: str) -> str:
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()


# ── Ollama backend ─────────────────────────────────────────────────────────────
def _chat_ollama(messages: list[dict]) -> str:
    import ollama
    resp = ollama.chat(model=LLM_MODEL, messages=messages)
    return _strip_think(resp["message"]["content"])


# ── OpenAI backend ─────────────────────────────────────────────────────────────
def _chat_openai(messages: list[dict]) -> str:
    from openai import OpenAI

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    resp = client.chat.completions.create(
        model=LLM_MODEL,
        messages=messages,
    )
    return _strip_think(resp.choices[0].message.content or "")


# ── Groq backend ──────────────────────────────────────────────────────────────
def _chat_groq(messages: list[dict]) -> str:
    from groq import Groq

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    resp = client.chat.completions.create(
        model=LLM_MODEL,
        messages=messages,
    )
    return _strip_think(resp.choices[0].message.content or "")


# ── Dispatcher ─────────────────────────────────────────────────────────────────
_BACKENDS = {
    "ollama": _chat_ollama,
    "openai": _chat_openai,
    "groq": _chat_groq,
}


def llm_chat(messages: list[dict]) -> str:
    """
    Send *messages* to the configured LLM backend and return the
    assistant's reply as a plain string.
    """
    backend = _BACKENDS.get(LLM_MODE)
    if backend is None:
        raise ValueError(
            f"Unknown LLM_MODE={LLM_MODE!r}. "
            f"Supported: {', '.join(_BACKENDS)}"
        )
    return backend(messages)
