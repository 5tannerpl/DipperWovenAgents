"""Workflow state definitions."""
from typing import TypedDict

from app.models.compliance_question import ComplianceQuestion
from app.models.understanding import (
    DetectedEntity,
    DetectedFact,
    IntendedAction,
)
from app.models.fact_context import (
    FactKey,
    RequiredFact,
    ResolvedFact,
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

    compliance_questions: list[ComplianceQuestion]

    # Phase 3
    required_facts: list[RequiredFact]
    resolved_facts: list[ResolvedFact]
    missing_facts: list[FactKey]
    fact_sufficient: bool

    