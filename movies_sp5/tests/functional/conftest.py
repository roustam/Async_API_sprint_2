import asyncio

import aiohttp
import pytest
import pytest_asyncio

pytest_plugins = ['es_client', 'redis_client', 'service_client']


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='session')
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()
