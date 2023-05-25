import json
from functools import lru_cache

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from redis.asyncio import Redis

from db.elastic import get_elastic
from db.redis import get_redis
from models.genre import Genre
from services.common import make_redis_key, CACHE_EXPIRE_IN_SECONDS


class GenreService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get(self, page: int, size: int) -> tuple[list[Genre], int]:
        genres_total = await self._get_genres_from_cache(page, size)

        if genres_total is None:
            genres_total = await self._get_genres_from_elastic(page, size)

            if genres_total is None:
                return [], 0

        genres, total = genres_total
        response = (genres, total)
        await self._put_genres_to_cache(response, page, size)

        return response

    async def _get_genres_from_cache(
        self, page: int, size: int
    ) -> tuple[list[Genre], int] | None:
        cache_key = make_redis_key('genres', page, size)
        cached_genres = await self.redis.get(cache_key)

        if not cached_genres:
            return None

        data = json.loads(cached_genres)
        genres_data = data["genres"]
        genres = [Genre(id=genre["id"], name=genre["name"]) for genre in genres_data]
        total = data["count"]

        return genres, total

    async def _get_genres_from_elastic(
        self, page: int, size: int
    ) -> tuple[list[Genre], int]:
        es_query = {
            "query": {"match_all": {}},
            "sort": [{"name.raw": "asc"}],
            "from": (page - 1) * size,
            "size": size,
        }
        result = await self.elastic.search(index="genres", body=es_query)
        total = result["hits"]["total"]["value"]

        genres = [
            Genre(id=genre["_id"], name=genre["_source"]["name"])
            for genre in result["hits"]["hits"]
        ]

        return genres, total

    async def _put_genres_to_cache(
        self, response: tuple[list[Genre], int], page: int, size: int
    ) -> None:
        cache_key = make_redis_key('genres', page, size)
        genres, total = response
        genres_data = [{"id": genre.id, "name": genre.name} for genre in genres]
        data = {"genres": genres_data, "count": total}
        await self.redis.set(cache_key, json.dumps(data), ex=CACHE_EXPIRE_IN_SECONDS)

    async def get_by_id(self, genre_id: str) -> Genre | None:
        genre = await self._get_genre_from_cache(genre_id)

        if not genre:
            genre = await self._get_genre_from_elastic_by_id(genre_id)

            if not genre:
                return None

            await self._put_genre_to_cache(genre)

        return genre


    async def _get_genre_from_elastic_by_id(self, genre_id: str) -> Genre | None:
        try:
            doc = await self.elastic.get("genres", genre_id)
        except NotFoundError:
            return None
        return Genre(**doc["_source"])

    async def _get_genre_from_cache(self, genre_id: str) -> Genre | None:
        cache_key = make_redis_key('genre', genre_id)
        cashed_genre = await self.redis.get(cache_key)

        if not cashed_genre:
            return None

        return Genre.parse_raw(cashed_genre)

    async def _put_genre_to_cache(self, genre: Genre):
        cache_key = make_redis_key('genre', genre.id)
        await self.redis.set(cache_key, genre.json(), ex=CACHE_EXPIRE_IN_SECONDS)


@lru_cache()
def get_genre_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(redis, elastic)
