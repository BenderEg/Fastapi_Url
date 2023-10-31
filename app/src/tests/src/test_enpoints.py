import json
import pytest
import pytest_asyncio

from tests.conftest import redis_client, session, make_get_request, \
    event_loop, make_post_request


@pytest.mark.asyncio
async def test_main_page_endpoint(make_get_request):
    body, status = await make_get_request('/')
    assert status == 200


@pytest.mark.asyncio
async def test_create_endpoint(make_post_request):
    body, status = await make_post_request(
        url='/create/',
        data=json.dumps({"incoming_link": "https://google.com/"}),
        headers={"Content-Type": "application/json"})
    assert status == 201