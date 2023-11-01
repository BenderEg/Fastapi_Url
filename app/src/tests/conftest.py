from json import JSONDecodeError
from typing import Optional

import asyncio
import pytest
import pytest_asyncio

from redis.asyncio import Redis
from httpx import AsyncClient

from core.config import settings
from db import redis
from main import app
from services.url import get_url_service, UrlService
from tests.utils.redis import get_redis_test


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
    red_client: Redis = await get_redis_test()
    yield red_client
    await red_client.flushdb()
    await red_client.aclose()


@pytest_asyncio.fixture(scope='module')
async def client() -> AsyncClient:
    app.dependency_overrides[redis.get_redis] = get_redis_test
    client = AsyncClient(app=app, base_url=f'http://{settings.domain}')
    yield client
    app.dependency_overrides = {}


@pytest_asyncio.fixture()
def make_get_request(client: AsyncClient) -> tuple:
    async def inner(url: str, path: Optional[str] = None):
        if path:
            url += f'/{path}'
        response = await client.get(url)
        status = response.status_code
        try:
            body = response.json()
        except JSONDecodeError:
            return None, status
        return body, status
    return inner


@pytest_asyncio.fixture()
def make_post_request(client: AsyncClient) -> tuple:
    async def inner(url: str, path: Optional[str] = None,
                    data: Optional[dict] = None,
                    headers: Optional[dict] = None):
        if path:
            url += f'/{path}'
        response = await client.post(url, data=data, headers=headers)
        status = response.status_code
        try:
            body = response.json()
        except JSONDecodeError:
            return None, status
        return body, status
    return inner