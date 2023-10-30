from functools import lru_cache
from random import choice, choices
from string import ascii_letters, digits

from fastapi import Depends
from redis.asyncio import Redis

from db.redis import get_redis
from models.url import UrlOut


class UrlService():

    def __init__(self, storage: Redis):
        self.storage = storage
        self.symbols = ascii_letters + digits

    def create_short_url(self, link: UrlOut) -> str:

        added_part = ''
        if link.path:
            path = link.path.strip('/')
            path = path.split('/')
            added_part += ''.join([choice(ele) for ele in path])
        if link.query:
            query = [ele.split('=') for ele in link.query.split('&')]
            query_dict = {ele[0]: ele[1] for ele in query}
            added_part += ''.join([choice(ele) for ele in query_dict.values() if ele != ''])
        random_part = choices(self.symbols, k=5)
        added_part += ''.join(random_part)
        return f'{link.host}/{added_part}'

    async def add_url_to_storage(self, key: str, value: str) -> None:

        await self.storage.set(key, value)

    async def get_url_from_storage(self, key: str) -> str:

        value = await self.storage.get(key)
        return value


@lru_cache()
def get_url_service(
        redis: Redis = Depends(get_redis)
) -> UrlService:
    return UrlService(redis)