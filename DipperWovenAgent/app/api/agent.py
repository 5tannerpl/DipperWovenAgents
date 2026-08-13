"""Agent API endpoints."""
import uuid

from fastapi import APIRouter

from app.models.request import AgentRequest
from app.orchestration.graph_builder import build_graph


router = APIRouter()

graph = build_graph()


@router.post("/invoke")
async def invoke_agent(
    request: AgentRequest
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

    return result