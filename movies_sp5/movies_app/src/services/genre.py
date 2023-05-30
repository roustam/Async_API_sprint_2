from functools import lru_cache

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
import orjson
from redis.asyncio import Redis

from db.elastic import get_elastic
from db.redis import get_redis
from models.genre import Genre
from services.common import make_redis_key, CACHE_EXPIRE_IN_SECONDS, ServiceAbstract


class GenreService(ServiceAbstract):
    async def get_by_id(self, genre_id: str) -> Genre | None:
        key = make_redis_key('genre', genre_id)
        genre = await self._get_genres_from_cache(key)
        if not genre:
            genre = await self._get_genre_from_elastic(genre_id)
            await self._save_genres_to_cache(key, genre)
        return Genre(**genre['_source']) if genre else None
    
    async def get(self, page_number: int | None = 1, page_size: int | None = 10) -> list[Genre]:
        key = make_redis_key('genres', page_number, page_size)
        genres = await self._get_genres_from_cache(key)
        if not genres:
            genres = await self._get_genres_from_elastic(page_number=page_number, page_size=page_size)
            await self._save_genres_to_cache(key, genres)
        return [Genre(**doc['_source']) for doc in genres['hits']['hits']]

    async def _get_genres_from_cache(self, key) -> dict | list[dict]:
        genres = await self.redis.get(key)
        return orjson.loads(genres) if genres else None
        
    async def _save_genres_to_cache(self, key, genres):
        await self.redis.set(key, orjson.dumps(genres.body).decode(), CACHE_EXPIRE_IN_SECONDS)

    async def _get_genre_from_elastic(self, genre_id: str) -> dict | None:
        try:
            return await self.elastic.get(index='genres', id=genre_id)
        except NotFoundError:
            return None

    async def _get_genres_from_elastic(
        self, page_number: int | None = 1, page_size: int | None = 10
    ) -> dict:
        body = {
            'query': {'match_all': {}},
            'sort': [{'name.raw': 'asc'}],
            'from': (page_number - 1) * page_size,
            'size': page_size,
        }
        return await self.elastic.search(index='genres', body=body)


@lru_cache()
def get_genre_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(redis, elastic)
