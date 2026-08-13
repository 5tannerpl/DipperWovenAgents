"""Models for case fact requirements and fact sufficiency."""

from typing import Literal

from pydantic import BaseModel, Field


FactKey = Literal[
    # Representative
    "customer_claimed_representative",
    "representative_type",
    "representative_identity",
    "representative_contact_details",
    "representative_record_exists",
    "representative_relates_to_debt",

    # Authority
    "authority_record_exists",
    "authority_received",
    "authority_verified",
    "authority_scope",
    "authority_current",

    # Communication
    "no_direct_contact_instruction",
    "previous_direct_contact",

    # Hardship
    "hardship_claim_exists",
    "hardship_status",
    "hardship_assessment_status",

    # Dispute
    "dispute_claim_exists",
    "dispute_status",

    # Complaint
    "complaint_claim_exists",
    "complaint_status",

    # Bankruptcy
    "bankruptcy_claim_exists",
    "bankruptcy_status",
    "trustee_exists",
    "trustee_identity",
    "trustee_authority",

    # Payment
    "payment_commitment_exists",
    "payment_commitment_status",
]


FactVerificationStatus = Literal[
    "unverified",
    "verified",
    "unresolved",
]


class RequiredFact(BaseModel):
    key: FactKey
    reason: str
    related_question_ids: list[str] = Field(
        default_factory=list
    )


class ResolvedFact(BaseModel):
    key: FactKey
    value: str | bool | None = None

    verification_status: FactVerificationStatus

    source: str | None = None
    source_record_id: str | None = None
    observed_at: str | None = None


class FactSufficiencyResult(BaseModel):
    sufficient: bool

    required_facts: list[RequiredFact] = Field(
        default_factory=list
    )

    resolved_facts: list[ResolvedFact] = Field(
        default_factory=list
    )

    missing_facts: list[FactKey] = Field(
        default_factory=list
    )