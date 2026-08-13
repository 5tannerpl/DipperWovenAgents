from typing import Literal

from pydantic import BaseModel, Field


ComplianceTopic = Literal[
    "representative_status",
    "authority",
    "direct_contact",
    "contact_exception",
    "payment_request",
    "privacy",

    "hardship_status",
    "hardship_assessment",
    "collection_during_hardship",

    "dispute_status",
    "collection_during_dispute",

    "complaint_status",

    "bankruptcy_status",
    "trustee_status",
    "collection_during_bankruptcy",

    "payment_arrangement_status",
]


class ComplianceQuestion(BaseModel):
    id: str
    topic: ComplianceTopic
    question: str


class ComplianceQuestionResult(BaseModel):
    questions: list[ComplianceQuestion] = Field(
        default_factory=list
    )