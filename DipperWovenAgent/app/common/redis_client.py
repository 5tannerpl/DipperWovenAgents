"""Shared asynchronous Redis client."""
import os

import redis.asyncio as redis


redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "rag-redis"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    password=os.getenv("REDIS_PASSWORD", "Ew27302-Dwoven"),
    db=0,
    decode_responses=True,
)