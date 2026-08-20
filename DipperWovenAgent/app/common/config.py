"""Application configuration."""

import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    LLM_PROVIDER: str = os.getenv(
        "LLM_PROVIDER",
        "openai"
    )

    OPENAI_API_KEY: str = os.getenv(
        "OPENAI_API_KEY",
        ""
    )

    OPENAI_MODEL: str = os.getenv(
        "OPENAI_MODEL",
        "gpt-5-mini"
    )

    LOCAL_BASE_URL: str = os.getenv(
        "LOCAL_BASE_URL",
        "http://127.0.0.1:11434/v1"
    )

    LOCAL_MODEL: str = os.getenv(
        "LOCAL_MODEL",
        "phi4-mini:latest"
    )


settings = Settings()
