from fastapi import FastAPI

from app.api.agent import router as agent_router

app = FastAPI(
    title="DipperWovenAgent",
    version="0.1.0"
)

app.include_router(
    agent_router,
    prefix="/api/agent",
    tags=["Agent"]
)


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "DipperWovenAgent"
    }