from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis

from api.v1 import url
from core.config import settings
from db import redis


@asynccontextmanager
async def lifespan(app: FastAPI):

    redis.redis_conn = Redis(host=settings.redis_host,
                       port=settings.redis_port,
                       db=settings.redis_db)
    yield
    await redis.redis_conn.close()


app = FastAPI(
    title="API для работы с ссылками",
    description="Позволяет получать сокращенные ссылки и дает по ним доступ к исходным ресурсам",
    version="1.0.0",
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    lifespan=lifespan
)

app.include_router(url.router, tags=['url'])
