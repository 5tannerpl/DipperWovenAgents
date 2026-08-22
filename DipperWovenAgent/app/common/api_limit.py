"""Global API quota dependency."""
from datetime import date

from fastapi import HTTPException, status

from app.common.redis_client import redis_client

DAILY_LLM_LIMIT = 100


async def check_global_api_limit() -> int:
    today_str = date.today().isoformat()
    redis_key = f"global_llm_daily_count:{today_str}"
    current_count = await redis_client.incr(redis_key)

    if current_count == 1:
        await redis_client.expire(redis_key, 86400)

    if current_count > DAILY_LLM_LIMIT:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail={
                "error": "Quota Exceeded",
                "message": (
                    f"Today's system API key quota ({DAILY_LLM_LIMIT}) has been "
                    "exhausted. Please try again tomorrow."
                ),
                "limit": DAILY_LLM_LIMIT,
                "current": current_count - 1,
            },
        )

    return current_count
