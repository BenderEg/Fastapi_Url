from typing import Optional

from redis.asyncio import Redis

redis_conn: Optional[Redis] = None

async def get_redis() -> Redis:
    return redis_conn