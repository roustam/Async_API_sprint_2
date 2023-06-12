import orjson
from redis.asyncio import Redis

from db.abstract import AsyncCacheStorage


CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут


redis: Redis | None = None


# Функция понадобится при внедрении зависимостей
async def get_redis() -> 'RedisClient':
    return RedisClient()


class RedisClient(AsyncCacheStorage):
    async def get_by_key(self, key) -> dict | list[dict]:
        data = await redis.get(key)
        return orjson.loads(data) if data else None
    
    async def save_by_key(self, key, data):
        await redis.set(key, orjson.dumps(data.body).decode(), CACHE_EXPIRE_IN_SECONDS)
