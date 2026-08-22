"""Agent API endpoints."""
import uuid

from fastapi import APIRouter, Depends, HTTPException
import asyncio
from app.repositories.debt_repository import debt_repository
from app.orchestration.prefetcher import prefetch_debt_context

from app.common.api_limit import check_global_api_limit
from app.models.request import AgentRequest
from app.models.compliance_question import ComplianceQuestionResult
from app.orchestration.graph_builder import build_graph
from app.integrations.debt_context_prefetch import prefetch_debt_context

router = APIRouter()

graph = build_graph()


@router.post("/invoke", response_model=ComplianceQuestionResult,)
async def invoke_agent(
    request: AgentRequest,
    _: int = Depends(check_global_api_limit),
):
    debt_id = await debt_repository.get_random_debt_id()

    if debt_id is None:
        raise HTTPException(
            status_code=404,
            detail="No debt_id available",
        )

    request_id = str(uuid.uuid4())

    prefetch_task = asyncio.create_task(
        prefetch_debt_context(
            request_id=request_id,
            debt_id=debt_id,
        )
    )

    initial_state = {
        "request_id": request_id,

        "case_id": debt_id,
        "target_type": request.target_type,
        "raw_input": request.content,

        "jurisdiction": request.jurisdiction,
        "region": request.region,
    }

    result = await graph.ainvoke(
        initial_state
    )

    return ComplianceQuestionResult(
        questions=result.get("compliance_questions", [])
    )
