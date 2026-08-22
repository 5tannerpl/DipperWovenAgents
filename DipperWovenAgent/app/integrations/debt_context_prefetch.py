import json
import logging

import httpx

from app.common.config import settings
from app.common.redis_client import redis_client


logger = logging.getLogger(__name__)

DEBT_CONTEXT_TTL_SECONDS = 120


def build_debt_context_key(request_id: str) -> str:
    return f"agent:debt-context:{request_id}"


async def prefetch_debt_context(
    request_id: str,
    debt_id: int,
) -> None:

    try:
        async with httpx.AsyncClient(
            base_url=settings.BUSINESS_API_BASE_URL,
            timeout=5.0,
        ) as client:

            response = await client.get(
                f"/internal/agent/debts/{debt_id}/summary"
            )

            response.raise_for_status()

            context = response.json()

        await redis_client.set(
            build_debt_context_key(request_id),
            json.dumps(
                context,
                ensure_ascii=False,
                default=str,
            ),
            ex=DEBT_CONTEXT_TTL_SECONDS,
        )

        logger.info(
            "Debt context prefetched. request_id=%s debt_id=%s",
            request_id,
            debt_id,
        )

    except Exception:
        logger.exception(
            "Debt context prefetch failed. request_id=%s debt_id=%s",
            request_id,
            debt_id,
        )