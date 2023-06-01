import asyncio
import uuid
import aiohttp
from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk
import pytest
import pytest_asyncio
from redis.asyncio import Redis

from .utils.helpers import gen_bulk_data, persons_bulk_data
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
    client = AsyncElasticsearch(
        hosts=[f"http://{elastic_settings.ELASTIC_HOST}:{elastic_settings.ELASTIC_PORT}"],
        verify_certs=False,
    )
    yield client
    await client.close()


@pytest_asyncio.fixture(scope='session')
async def redis_client():
    client = Redis(host=redis_settings.REDIS_HOST, port=redis_settings.REDIS_PORT)
    yield client
    await client.close()


@pytest_asyncio.fixture(scope='session')
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest_asyncio.fixture
async def es_write_data(es_client: AsyncElasticsearch):
    async def inner(index: str, data: list, id: str):
        bulk_data = gen_bulk_data(index=index, persons=data, id_field=id)
        response = await async_bulk(es_client, bulk_data)

        if response[0] == 0:
            raise Exception('Ошибка записи данных в Elasticsearch')

    yield inner

    await es_client.delete_by_query(index='_all', body={"query": {"match_all": {}}})


@pytest_asyncio.fixture
async def es_write_persons(es_client: AsyncElasticsearch):
    async def inner(index: str, data: list, id: str):
        bulk_data = persons_bulk_data(index=index, persons=data, id_field=id)
        response = await async_bulk(es_client, bulk_data)

        if response[0] == 0:
            raise Exception('Ошибка записи данных в Elasticsearch')

    yield inner

    await es_client.delete_by_query(index='persons', body={"query": {
        "match_all": {}}})


@pytest_asyncio.fixture
async def make_get_request(session: aiohttp.ClientSession, redis_client: Redis):
    async def inner(handler: str, data: dict = None):

        async with session.get(f'http://{app_settings.APP_HOST}:{app_settings.APP_PORT}' + '/api/v1' + handler,
                               params=data) as response:
            if response.status == 200:
                return await response.json()
            else:
                raise Exception(response)
    yield inner
    await redis_client.flushdb()


@pytest_asyncio.fixture
async def get_api_response(session: aiohttp.ClientSession, redis_client:
Redis):
    async def inner(handler: str, data: dict = None):

        async with session.get(f'http://{app_settings.APP_HOST}:{app_settings.APP_PORT}' + '/api/v1' + handler,
                               params=data) as response:
            if response.status == 200:
                return response.status, await response.json()
            else:
                raise Exception(response)
    yield inner
    await redis_client.flushdb()

@pytest.fixture
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



