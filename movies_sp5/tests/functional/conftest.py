import asyncio
import datetime
import uuid
import aiohttp
from elasticsearch import AsyncElasticsearch
import pytest
import pytest_asyncio

from settings import elastic_settings
from settings import app_settings
from utils.helpers import get_es_bulk_query


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='session')
async def es_client():
    client = AsyncElasticsearch(
        hosts=[f"{elastic_settings.ELASTIC_HOST}:{elastic_settings.ELASTIC_PORT}"],
        validate_cert=False,
        use_ssl=False,
    )
    yield client
    await client.close()


@pytest_asyncio.fixture(scope='session')
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture
def es_write_data(es_client: AsyncElasticsearch):
    async def inner(data: list[dict], index: str, id_field: str):
        bulk_query = get_es_bulk_query(data, index, id_field)
        str_query = '\n'.join(bulk_query) + '\n'
        response = await es_client.bulk(str_query, refresh=True)
        if response['errors']:
            raise Exception('Ошибка записи данных в Elasticsearch')
    return inner


@pytest.fixture
def make_get_request(session: aiohttp.ClientSession):
    async def inner(handler: str, data: dict):
        async with session.get(f'http://{app_settings.APP_HOST}:{app_settings.APP_PORT}' + '/api/v1' + handler, params=data) as response:
            status = response.status
            if status == 200:
                body = await response.json()
            else:
                raise Exception(response)
            return status, body 
    return inner


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
        } for _ in range(60)
    ]
