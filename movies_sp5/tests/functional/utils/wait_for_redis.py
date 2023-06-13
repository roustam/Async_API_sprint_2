import asyncio
import logging
from redis.asyncio import Redis
import traceback

from settings import redis_settings

async def wait_redis(redis_client: Redis, 
                     start_sleep_time=0.1, factor=2, border_sleep_time=10.0):
    n = 0
    t = start_sleep_time
    while True:
        try:
            if await redis_client.ping():
                break
            elif t == border_sleep_time:
                logging.error(f'Border time exceeded after {n} attempts')
                break
            else:
                t = start_sleep_time * (factor**n) if t < border_sleep_time else border_sleep_time
                await asyncio.sleep(t)
        except Exception as err:
            logging.error(err)
            logging.error(traceback.format_exc())


if __name__ == '__main__':
    redis_client = Redis(host=redis_settings.REDIS_HOST, port=redis_settings.REDIS_PORT)
    asyncio.run(wait_redis(redis_client))
