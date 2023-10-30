from datetime import datetime
from functools import lru_cache
from random import choices

from fastapi import Depends
from redis.asyncio import Redis

from db.redis import get_redis


class UrlService():

    def __init__(self, storage: Redis):
        self.storage = storage
        self.symbols = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.mod = len(self.symbols)

    def create_short_url(self, stamp: datetime) -> str:

        added_part = ''
        data = (stamp.year, stamp.month, stamp.day, stamp.hour,
                stamp.minute, stamp.second, stamp.microsecond)
        for ele in data:
            value = ele%self.mod
            added_part += self.symbols[value]
        random_part = choices(self.symbols, k=5)
        added_part += ''.join(random_part)
        return added_part

    async def add_url_to_storage(self, key: str, value: str) -> None:

        await self.storage.set(key, value)

    async def add_original_url_to_storage(self, key: str, value: str,
                                          expire: int) -> None:

        await self.storage.set(key, value, expire)

    async def get_from_storage(self, key: str) -> str:

        value = await self.storage.get(key)
        return value

    async def hash_link(self, link: str) -> int:
        return hash(link)


@lru_cache()
def get_url_service(
        redis: Redis = Depends(get_redis)
) -> UrlService:
    return UrlService(redis)