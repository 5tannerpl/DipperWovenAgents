"""Application configuration."""

import os

from dotenv import load_dotenv


load_dotenv()


class Settings:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

    OPENAI_MODEL: str = os.getenv(
        "OPENAI_MODEL",
        "gpt-5-mini"
    )

    LOCAL_MODEL: str = os.getenv(
        "LOCAL_MODEL",
        "phi4-mini"
    )


settings = Settings()
