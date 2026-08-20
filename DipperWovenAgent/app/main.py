from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.agent import router as agent_router
from app.common.api_limit import DAILY_LLM_LIMIT, check_global_api_limit

app = FastAPI(
    title="DipperWovenAgent",
    version="0.1.0",
    docs_url="/agent/docs",
    redoc_url=None,
    openapi_url="/agent/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:62969",
        "https://localhost:62969",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    agent_router,
    prefix="/api/agent",
    tags=["Agent"]
)

@app.get("/health")
async def health(count: int = Depends(check_global_api_limit)):
    return {
        "status": "ok",
        "service": "rag-api",
        "usage": f"Today's usage: {count}/{DAILY_LLM_LIMIT}"
    }
