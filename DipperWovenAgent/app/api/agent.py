"""Agent API endpoints."""
import uuid

from fastapi import APIRouter, Depends

from app.common.api_limit import check_global_api_limit
from app.models.request import AgentRequest
from app.models.compliance_question import ComplianceQuestionResult
from app.orchestration.graph_builder import build_graph


router = APIRouter()

graph = build_graph()


@router.post("/invoke"，response_model=ComplianceQuestionsResult,)
async def invoke_agent(
    request: AgentRequest,
    _: int = Depends(check_global_api_limit),
):

    initial_state = {
        "request_id": str(uuid.uuid4()),

        "case_id": request.case_id,
        "target_type": request.target_type,
        "raw_input": request.content,

        "jurisdiction": request.jurisdiction,
        "region": request.region,
    }

    result = await graph.ainvoke(
        initial_state
    )

    return ComplianceQuestionsResult(
    compliance_questions=result.get("compliance_questions", [])
    )
