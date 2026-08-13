"""Workflow state definitions."""
from typing import TypedDict

from app.models.understanding import (
    DetectedEntity,
    DetectedFact,
    IntendedAction,
)


class DipperWovenAgentState(TypedDict, total=False):
    request_id: str

    case_id: str
    target_type: str
    raw_input: str

    jurisdiction: str
    region: str

    normalized_input: str

    detected_facts: list[DetectedFact]
    intended_actions: list[IntendedAction]
    detected_events: list[str]
    entities: list[DetectedEntity]