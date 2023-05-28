from functools import lru_cache

import orjson
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from redis.asyncio import Redis

from db.elastic import get_elastic
from db.redis import get_redis
from models.film import Film
from services.common import make_redis_key

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут


class FilmService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_by_id(self, film_id: str) -> Film | None:
        key = make_redis_key('film', film_id)
        film = await self._get_films_from_cache(key)
        if not film:
            film = await self._get_film_from_elastic(film_id)
            await self._save_films_to_cache(key, film)
        return Film(**film["_source"]) if film else None

    async def get(self, sort: str, genre_id: str | None = None, page_number: int | None = 1, page_size: int | None = 10) -> list[Film]:
        key = make_redis_key('films', sort, genre_id, page_number, page_size)
        films = await self._get_films_from_cache(key)
        if not films:
            films = await self._get_films_from_elastic(sort=sort, genre_id=genre_id, page_number=page_number, page_size=page_size)
            await self._save_films_to_cache(key, films)
        return [Film(**doc["_source"]) for doc in films["hits"]["hits"]]

    async def search(self, query: str, page_number: int | None = 1, page_size: int | None = 10) -> list[Film]:
        key = make_redis_key('films', query, page_number, page_size)
        films = await self._get_films_from_cache(key)
        if not films:
            films = await self._search_films_in_elastic(query, page_number=page_number, page_size=page_size)
            await self._save_films_to_cache(key, films)
        return [Film(**doc["_source"]) for doc in films["hits"]["hits"]]
    
    async def _get_films_from_cache(self, key):
        films = await self.redis.get(key)
        return orjson.loads(films) if films else None
        
    async def _save_films_to_cache(self, key, films):
        await self.redis.set(key, orjson.dumps(films).decode(), FILM_CACHE_EXPIRE_IN_SECONDS)

    async def _get_film_from_elastic(self, film_id: str) -> Film | None:
        try:
            #refactoring according Elastic 8.x version
            return await self.elastic.get(index="movies", id=film_id)
        except NotFoundError:
            return None

    async def _get_films_from_elastic(
        self, sort: str, genre_id: str | None = None, page_number: int | None = 1, page_size: int | None = 10
    ):
        first_symbol = sort[0]
        if first_symbol.isalpha():
            sort_field = sort
            sort_order = "asc"
        else:
            sort_field = sort[1:]
            sort_order = "desc" if first_symbol == "-" else "asc"

        body = {
            "sort": [{sort_field: sort_order}],
            "from": (page_number - 1) * page_size,
            "size": page_size,
        }
        if genre_id:
            body |= {
                "query": {
                    "nested": {
                        "path": "genres",
                        "query": {"term": {"genres.id": {"value": genre_id}}},
                    }
                },
            }
            
        return await self.elastic.search(query=body, index="movies")

    async def _search_films_in_elastic(self, query: str, page_number: int | None = 1, page_size: int | None = 10):
        return await self.elastic.search(
            query = {
                "query": {
                    "multi_match": {
                        "query": query,
                        "fuzziness": "auto",
                        "fields": [
                            "actors_names",
                            "writers_names",
                            "title",
                            "description",
                            "genres",
                        ],
                    }
                },
                "from": (page_number - 1) * page_size,
                "size": page_size,
            },
            index="movies"
        )


@lru_cache()
def get_film_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic)
