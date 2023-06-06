import asyncio
import uuid
import aiohttp
from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk
import pytest
import pytest_asyncio
from redis.asyncio import Redis

from typing import Iterable, Any
from .utils.helpers import gen_bulk_data, prepare_bulk_data, get_es_bulk_query
from .testdata.genres import get_all_genres
from .testdata.films import random_films
from .utils.helpers import gen_bulk_data, persons_bulk_data, person_movies_bulk_data
from .settings import elastic_settings
from .settings import app_settings
from .settings import redis_settings


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='session')
async def es_client():
    client = AsyncElasticsearch(hosts=[
            f"http://{elastic_settings.ELASTIC_HOST}:{elastic_settings.ELASTIC_PORT}"],
        verify_certs=False,
        request_timeout=30
    )
    yield client
    await client.close()


@pytest_asyncio.fixture(scope='session')
async def redis_client():
    client = Redis(
        host=redis_settings.REDIS_HOST, port=redis_settings.REDIS_PORT)
    yield client
    await client.close()


@pytest_asyncio.fixture(scope='session')
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest_asyncio.fixture(scope='session')
async def es_write_data(es_client: AsyncElasticsearch):
    async def inner(index: str, data: list):
        ready_bulk_data = prepare_bulk_data(index=index, data=data)
        response = await es_client.bulk(index=index, operations=ready_bulk_data)
        if not response:
            raise Exception('Ошибка записи данных в Elasticsearch')
    return inner


@pytest_asyncio.fixture(scope='session')
async def es_remove_data(es_client: AsyncElasticsearch):
    async def inner(index: str):
        await es_client.delete_by_query(index=index,
                                    query={"match_all": {}},
                                    wait_for_completion=True,
                                    requests_per_second=1,
                                    )
    return inner


# @pytest_asyncio.fixture
# async def es_add_bulk_data(es_client: AsyncElasticsearch):
#     async def inner(index: str, qu: list[dict]):
#         response = await es_client.bulk(index=index, query=qu)
#     await es_client.delete_by_query(index=['movies','persons','genres'],
#                                     query={"match_all": {}},
#                                     wait_for_active_shards=1)

@pytest_asyncio.fixture
async def es_write_persons(es_client: AsyncElasticsearch):
    async def inner(index: str, data: list, id: str):
        bulk_data = persons_bulk_data(index=index, persons=data, id_field=id)
        response = await async_bulk(es_client, bulk_data)

        if response[0] == 0:
            raise Exception('Ошибка записи данных в Elasticsearch')

    yield inner

    await es_client.delete_by_query(
        index='persons', query={"match_all": {}})


<<<<<<< HEAD

@pytest_asyncio.fixture(scope='session')
async def make_get_request(session: aiohttp.ClientSession, redis_client: Redis):
    async def inner(handler: str, data: dict = None):
        url = f'http://{app_settings.APP_HOST}:{app_settings.APP_PORT}'
        async with session.get(url + '/api/v1' + handler, params=data) as response:
=======
@pytest_asyncio.fixture
async def es_write_person_movies(es_client: AsyncElasticsearch):
    async def inner(index: str, data: list[dict], id: str):
        bulk_data = person_movies_bulk_data(
            index=index,
            movies=data,
            id_field=id
        )
        response = await async_bulk(es_client, bulk_data)

        if response[0] == 0:
            raise Exception('Ошибка записи данных в Elasticsearch')

    yield inner

    await es_client.delete_by_query(
        index='movies', query={"match_all": {}})


@pytest_asyncio.fixture
async def make_get_request(
        session: aiohttp.ClientSession, redis_client: Redis
):
    async def inner(handler: str, data: dict = None):
        async with session.get(
                f'http://{app_settings.APP_HOST}:{app_settings.APP_PORT}' + '/api/v1' + handler,
                params=data) as response:
>>>>>>> 231478ce4dca793b352765dfcf292e8a394d7240
            if response.status == 200:
                return await response.json()
            else:
                raise Exception(response)
<<<<<<< HEAD
    return inner


@pytest_asyncio.fixture(scope='session')
async def flush_cache(redis_client: Redis):
    async def inner():
        result = await redis_client.flushdb()
        return result
    return inner

@pytest.fixture(scope='session')
def get_genres():
    return get_all_genres()
=======

    yield inner
    await redis_client.flushdb()


@pytest_asyncio.fixture
async def get_api_response(
        session: aiohttp.ClientSession, redis_client:
        Redis
):
    async def inner(handler: str, data: dict = None):
        async with session.get(
                f'http://{app_settings.APP_HOST}:{app_settings.APP_PORT}' + '/api/v1' + handler,
                params=data) as response:
            if response.status == 200:
                return response.status, await response.json()
            else:
                raise Exception(response)

    yield inner
    await redis_client.flushdb()
>>>>>>> 231478ce4dca793b352765dfcf292e8a394d7240

@pytest.fixture(scope='session')
def get_films():
    return random_films(10)

@pytest.fixture(scope='session')
def es_data():
    return [
        {
            'id': str(uuid.uuid4()),
            'imdb_rating': 8.5,
            'genres': [
                {
                    'id': str(uuid.uuid4()),
                    'name': 'Action'
                },
                {
                    'id': str(uuid.uuid4()),
                    'name': 'Sci-Fi'
                }
            ],
            'title': 'The Star',
            'description': 'New World',
            'directors_names': ['Alise', 'John'],
            'actors_names': ['Ann', 'Bob'],
            'writers_names': ['Ben', 'Howard'],
            'actors': [
                {'id': '111', 'name': 'Ann'},
                {'id': '222', 'name': 'Bob'}
            ],
            'writers': [
                {'id': '333', 'name': 'Ben'},
                {'id': '444', 'name': 'Howard'}
            ],
            'directors': [
                {'id': '555', 'name': 'Alise'},
                {'id': '666', 'name': 'John'}
            ],
        } for _ in range(15)
    ]
