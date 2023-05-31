from functools import lru_cache

from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.genre import Genre
from db.elastic import ElasticClient
from db.redis import RedisClient
from services.common import make_redis_key, ServiceAbstract


class GenreService(ServiceAbstract):
    async def get_by_id(self, genre_id: str) -> Genre | None:
        key = make_redis_key('genre', genre_id)
        genre = await self.redis.get_by_key(key)
        if not genre:
            genre = await self.elastic.get_by_id('genres', genre_id)
            await self.redis.save_by_key(key, genre)
        return Genre(**genre['_source']) if genre else None
    
    async def get(self, page_number: int | None = 1, page_size: int | None = 10) -> list[Genre]:
        key = make_redis_key('genres', page_number, page_size)
        genres = await self.redis.get_by_key(key)
        if not genres:
            genres = await self._get_genres_from_elastic(page_number=page_number, page_size=page_size)
            await self.redis.save_by_key(key, genres)
        return [Genre(**doc['_source']) for doc in genres['hits']['hits']]

    async def _get_genres_from_elastic(
        self, page_number: int | None = 1, page_size: int | None = 10
    ) -> dict:
        body = {
            'query': {'match_all': {}},
            'sort': [{'name.raw': 'asc'}],
        }
        return await self.elastic.search_by_query_with_pagination(
            index='genres',
            body=body,
            page_number=page_number,
            page_size=page_size,
        )


@lru_cache()
def get_genre_service(
    redis: RedisClient = Depends(get_redis),
    elastic: ElasticClient = Depends(get_elastic),
) -> GenreService:
    return GenreService(redis, elastic)
