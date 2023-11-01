import json
import pytest

from core.config import settings
from tests.conftest import redis_client, make_get_request, \
    event_loop, make_post_request, client
from tests.data.data import parameters_create, parameters_get, \
    parameters_get_not, parameters_count


@pytest.mark.asyncio
async def test_main_page_endpoint(make_get_request):
    _, status = await make_get_request('/')
    assert status == 200


@pytest.mark.parametrize('inpt, expected_answer', parameters_create)
@pytest.mark.asyncio
async def test_create_endpoint(make_post_request, redis_client,
                               inpt, expected_answer):
    body, status = await make_post_request(
        url='/create/',
        data=json.dumps(inpt),
        headers={"Content-Type": "application/json"})
    body_repeat, status_repeat = await make_post_request(
        url='/create/',
        data=json.dumps(inpt),
        headers={"Content-Type": "application/json"})
    link = body.split('/')[1]
    link_from_db = await redis_client.hget(name=link,
                                           key='value')
    link_repeat = body_repeat.split('/')[1]
    link_from_db_repeat = await redis_client.hget(name=link_repeat,
                                           key='value')
    assert status == 201
    assert link_from_db == expected_answer
    assert status_repeat == 201
    assert link_from_db == link_from_db_repeat


@pytest.mark.parametrize('inpt, expected_answer', parameters_get)
@pytest.mark.asyncio
async def test_get_link_in_db_endpoint(make_get_request, redis_client,
                                 inpt, expected_answer):
    await redis_client.hset(name=inpt["to_cache"],
                            mapping={'value': inpt['value'],
                                     'counter': 0})
    _, status = await make_get_request(inpt["to_cache"])
    assert status == expected_answer


@pytest.mark.parametrize('inpt, expected_answer', parameters_get_not)
@pytest.mark.asyncio
async def test_get_link_not_in_db_endpoint(make_get_request,
                                 inpt, expected_answer):
    _, status = await make_get_request(inpt)
    assert status == expected_answer


@pytest.mark.parametrize('inpt, expected_answer', parameters_count)
@pytest.mark.asyncio
async def test_count(make_get_request,
                     inpt, expected_answer):
    _, _ = await make_get_request(inpt)
    inpt += '+'
    body, status = await make_get_request(inpt)
    assert status == expected_answer