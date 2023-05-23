import asyncio

from elasticsearch import AsyncElasticsearch

from settings import elastic_settings


async def wait_es(es_client: AsyncElasticsearch):
    while True:
        if await es_client.ping():
            break
        await asyncio.sleep(1)


if __name__ == '__main__':
    es_client = AsyncElasticsearch(hosts=[f"{elastic_settings.ELASTIC_HOST}:{elastic_settings.ELASTIC_PORT}"], validate_cert=False, use_ssl=False)
    asyncio.run(wait_es(es_client))
