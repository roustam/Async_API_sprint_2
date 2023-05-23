import asyncio

from redis.asyncio import Redis

from settings import redis_settings


async def wait_redis(redis_client: Redis):
    while True:
        if await redis_client.ping():
            break
        await asyncio.sleep(1)


if __name__ == '__main__':
    redis_client = Redis(host=redis_settings.REDIS_HOST, port=redis_settings.REDIS_PORT)
    asyncio.run(wait_redis(redis_client))
