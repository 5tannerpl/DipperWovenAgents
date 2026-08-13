from typing import Literal

from pydantic import BaseModel, Field

FactType = Literal[
    "representative_claim",
    "hardship_claim",
    "bankruptcy_claim",
    "debt_agreement_claim",
    "dispute_claim",
    "complaint_claim",
    "vulnerability_claim",
    "payment_commitment",
    "contact_attempt_no_answer",
    "message_no_response",
    "missed_payment_commitment",
]

ActionType = Literal[
    "call_customer",
    "send_sms",
    "send_email",
    "request_payment",
    "create_payment_arrangement",
]

ActionPurpose = Literal[
    "request_payment",
    "verify_information",
    "discuss_account",
    "follow_up",
    "provide_document",
]

EntityType = Literal[
    "customer",
    "representative",
    "representative_type",
    "organisation",
    "amount",
    "date",
]

VerificationStatus = Literal[
    "unverified",
    "verified",
    "unknown",
]


DetectedEvent = Literal[
    "POTENTIAL_REPRESENTATIVE",
    "PROPOSED_DIRECT_CONTACT",
    "BANKRUPTCY",
    "DEBT_AGREEMENT",
    "HARDSHIP",
    "VULNERABILITY",
    "DISPUTE",
    "COMPLAINT",
    "DECEASED",
    "LEGAL_PROCEEDING",
    "PAYMENT_ARRANGEMENT",
    "MISSED_PAYMENT_COMMITMENT",
]


class DetectedFact(BaseModel):
    type: FactType
    value: str
    verification_status: VerificationStatus = "unverified"


class IntendedAction(BaseModel):
    action: ActionType
    purpose: ActionPurpose | None = None
    when: str | None = None


class DetectedEntity(BaseModel):
    type: EntityType
    value: str


class UnderstandingResult(BaseModel):
    facts: list[DetectedFact] = Field(default_factory=list)

    intended_actions: list[IntendedAction] = Field(
        default_factory=list
    )

    detected_events: list[DetectedEvent] = Field(
        default_factory=list
    )

    entities: list[DetectedEntity] = Field(
        default_factory=list
    )