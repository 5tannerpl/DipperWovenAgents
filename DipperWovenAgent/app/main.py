import os
from datetime import date
from fastapi import FastAPI, HTTPException, Depends, status
import redis.asyncio as redis

from app.api.agent import router as agent_router

app = FastAPI(
    title="DipperWovenAgent",
    version="0.1.0",
    docs_url="/agent/docs",
    redoc_url=None,
    openapi_url="/agent/openapi.json",
)

app.include_router(
    agent_router,
    prefix="/api/agent",
    tags=["Agent"]
)

REDIS_HOST = os.getenv("REDIS_HOST", "rag-redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)

DAILY_LLM_LIMIT = 100

async def check_global_api_limit():
    today_str = date.today().isoformat()  # 获取当前日期 '2026-08-18'
    redis_key = f"global_llm_daily_count:{today_str}"

    # Redis 自增 1
    current_count = await redis_client.incr(redis_key)

    # 如果是今天第 1 次调用，设置 24 小时 (86400秒) 过期，自动清理旧 key
    if current_count == 1:
        await redis_client.expire(redis_key, 86400)

    # 达到 100 次上限，立即拦截
    if current_count > DAILY_LLM_LIMIT:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail={
                "error": "Quota Exceeded",
                "message": f"今日系统的 API Key 调用总额度（{DAILY_LLM_LIMIT}次）已用尽，请明天再试。",
                "limit": DAILY_LLM_LIMIT,
                "current": current_count - 1
            }
        )
    return True

@app.get("/health")
async def health(count: int = Depends(check_global_api_limit)):
    return {
        "status": "ok",
        "service": "rag-api",
        "usage": f"Today's usage: {count}/{DAILY_LLM_LIMIT}"
    }
