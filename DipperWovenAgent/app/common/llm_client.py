"""Shared LLM client."""

from openai import AsyncOpenAI

from app.common.config import settings


if not settings.OPENAI_API_KEY:
    raise RuntimeError(
        "OPENAI_API_KEY is not configured."
    )


llm_client = AsyncOpenAI(
    api_key=settings.OPENAI_API_KEY
)

local_llm_client = AsyncOpenAI(
    api_key="ollama",
    base_url="http://localhost:11434/v1"
)
