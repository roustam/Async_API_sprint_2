import pytest_asyncio
from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk

from utils.helpers import person_movies_bulk_data, persons_bulk_data, prepare_bulk_data

from settings import elastic_settings


@pytest_asyncio.fixture(scope='session')
async def es_client():
    client = AsyncElasticsearch(hosts=[
            f"http://{elastic_settings.ELASTIC_HOST}:{elastic_settings.ELASTIC_PORT}"],
        verify_certs=False,
        request_timeout=30,

    )
    yield client
    await client.close()


@pytest_asyncio.fixture(scope='session')
async def es_write_data(es_client: AsyncElasticsearch):
    async def inner(index: str, data: list):
        ready_bulk_data = prepare_bulk_data(index=index, data=data)
        response = await es_client.bulk(index=index,refresh=True,
                                        operations=ready_bulk_data)
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


@pytest_asyncio.fixture(scope='session')
async def clean_elasticsearch(es_client: AsyncElasticsearch):
    async def inner(index: str):
        res = await es_client.delete_by_query(index=index,
                                        query={"match_all": {}},
                                        requests_per_second=3,
                                        wait_for_completion=True
                                        )
        return res

    return inner


@pytest_asyncio.fixture
async def es_write_persons(es_client: AsyncElasticsearch):
    async def inner(index: str, data: list, id: str):
        bulk_data = persons_bulk_data(index=index, persons=data, id_field=id)
        response = await async_bulk(es_client, bulk_data)

        if response[0] == 0:
            raise Exception('Ошибка записи данных в Elasticsearch')

    return inner


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

    return inner
