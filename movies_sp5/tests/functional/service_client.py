import aiohttp
import pytest
from redis import Redis
from testdata.films import random_films
from testdata.genres import get_all_genres
import pytest_asyncio

from settings import app_settings


@pytest_asyncio.fixture
async def make_get_request(session: aiohttp.ClientSession, redis_client: Redis):
    async def inner(handler: str, data: dict = None):
        async with session.get(
            f'http://{app_settings.APP_HOST}:{app_settings.APP_PORT}' + '/api/v1' + handler,
            params=data,
        ) as response:
            if response.status == 200:
                return await response.json()
            else:
                raise Exception(response)
    return inner


@pytest.fixture(scope='session')
def get_genres():
    return get_all_genres()


@pytest_asyncio.fixture
async def get_api_response(session: aiohttp.ClientSession, redis_client: Redis):
    async def inner(handler: str, data: dict = None):
        async with session.get(
            f'http://{app_settings.APP_HOST}:{app_settings.APP_PORT}' + '/api/v1' + handler,
            params=data
        ) as response:
            if response.status == 200:
                return response.status, await response.json()
            else:
                raise Exception(response)

    return inner


@pytest.fixture(scope='session')
def get_films():
    return random_films(3)


@pytest.fixture(scope='session')
def search_film_data():
    return random_films(10)
