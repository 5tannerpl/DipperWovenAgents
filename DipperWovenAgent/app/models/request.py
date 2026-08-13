from typing import Any

from pydantic import BaseModel, Field


class AgentRequest(BaseModel):
    case_id: str
    target_type: str = "note"
    content: str = Field(min_length=1)

    jurisdiction: str = "AU"
    region: str = "AU"

    metadata: dict[str, Any] = {}