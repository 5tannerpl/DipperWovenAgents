"""Application configuration."""

import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
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
        "http://host.docker.internal:11434/v1"
    )

    LOCAL_MODEL: str = os.getenv(
        "LOCAL_MODEL",
        "phi4-mini:latest"
    )

    AGENT_DB_HOST: str = "rag-postgres"
    AGENT_DB_PORT: int = 5432
    AGENT_DB_NAME: str = "ragdbDwoven"
    AGENT_DB_USER: str = "raguserDwoven"
    AGENT_DB_PASSWORD: str = "Ew27301-Dwoven"

    # C# Business System internal API
    BUSINESS_API_BASE_URL: str = os.getenv(
        "BUSINESS_API_BASE_URL",
        "http://host.docker.internal:8080"
    )


settings = Settings()
