from typing import Optional

import asyncio
import pytest
import pytest_asyncio

from aiohttp import ClientSession, ContentTypeError
from redis.asyncio import Redis

from core.config import settings
from services.url import get_url_service, UrlService


@pytest_asyncio.fixture(scope="module")
def event_loop() -> asyncio.AbstractEventLoop:
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='module')
def class_service() -> UrlService:
    url_service = get_url_service()
    yield url_service


@pytest_asyncio.fixture(scope='module')
async def redis_client() -> Redis:
    db_num = settings.redis_db+1
    red_client = Redis(host=settings.redis_host,
                       port=settings.redis_port,
                       db=db_num)
    yield red_client
    await red_client.flushdb()
    await red_client.close()


@pytest_asyncio.fixture(scope='module')
async def session() -> ClientSession:
    session = ClientSession()
    yield session
    await session.close()

@pytest_asyncio.fixture()
def make_get_request(session: ClientSession) -> tuple:
    async def inner(url: str, path: Optional[str] = None):
        url = f'http://{settings.domain}' + url
        if path:
            url += f'/{path}'
        async with session.get(url) as response:
            status = response.status
            try:
                body = await response.json()
            except ContentTypeError:
                return None, status
        return body, status
    return inner

@pytest_asyncio.fixture()
def make_post_request(session: ClientSession) -> tuple:
    async def inner(url: str, path: Optional[str] = None,
                    data: Optional[dict] = None,
                    headers: Optional[dict] = None):
        url = f'http://{settings.domain}' + url
        if path:
            url += f'/{path}'
        async with session.post(url, data=data, headers=headers) as response:
            status = response.status
            try:
                body = await response.json()
                print(body)
            except ContentTypeError:
                return None, status
        return body, status
    return inner