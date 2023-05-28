import asyncio

from elasticsearch import AsyncElasticsearch

from settings import elastic_settings


async def wait_es(es_client: AsyncElasticsearch):
    while True:
        if await es_client.ping():
            break
        await asyncio.sleep(1)


if __name__ == '__main__':
    es_client = AsyncElasticsearch(hosts=[f"http://{elastic_settings.ELASTIC_HOST}:"
                                          f"{elastic_settings.ELASTIC_PORT}"], verify_certs=False)
    asyncio.run(wait_es(es_client))
