"""Shared LLM client."""

from openai import AsyncOpenAI

from app.common.config import settings


if settings.LLM_PROVIDER == "openai":

    if not settings.OPENAI_API_KEY:
        raise RuntimeError(
            "OPENAI_API_KEY is not configured."
        )

    llm_client = AsyncOpenAI(
        api_key=settings.OPENAI_API_KEY
    )

    llm_model = settings.OPENAI_MODEL


elif settings.LLM_PROVIDER == "local":

    llm_client = AsyncOpenAI(
        api_key="ollama",
        base_url=settings.LOCAL_BASE_URL
    )

    llm_model = settings.LOCAL_MODEL


else:
    raise RuntimeError(
        f"Unsupported LLM_PROVIDER: {settings.LLM_PROVIDER}"
    )
