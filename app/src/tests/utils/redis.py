from typing import Optional

from redis.asyncio import Redis

from core.config import settings

redis_conn: Optional[Redis] = None

async def get_redis_test() -> Redis:
    global redis_conn
    if redis_conn:
        return redis_conn
    db_num = settings.redis_db+1
    redis_conn = Redis(host=settings.redis_host,
                       port=settings.redis_port,
                       db=db_num,
                       decode_responses=True)
    return redis_conn