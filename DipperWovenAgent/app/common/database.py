import asyncpg

from app.common.config import settings


_pool: asyncpg.Pool | None = None


async def init_db_pool():
    global _pool

    _pool = await asyncpg.create_pool(
        host=settings.AGENT_DB_HOST,
        port=settings.AGENT_DB_PORT,
        database=settings.AGENT_DB_NAME,
        user=settings.AGENT_DB_USER,
        password=settings.AGENT_DB_PASSWORD,
        min_size=1,
        max_size=5,
    )


async def close_db_pool():
    global _pool

    if _pool is not None:
        await _pool.close()


def get_db_pool() -> asyncpg.Pool:
    if _pool is None:
        raise RuntimeError("Database pool is not initialized")

    return _pool