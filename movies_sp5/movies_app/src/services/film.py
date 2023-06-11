from functools import lru_cache

from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.film import Film
from db.elastic import ElasticClient
from db.redis import RedisClient
from services.common import make_redis_key, ServiceAbstract


class FilmService(ServiceAbstract):
    async def get_by_id(self, film_id: str) -> Film | None:
        key = make_redis_key('film', film_id)
        film = await self.redis.get_by_key(key)
        if not film:
            film = await self.elastic.get_by_id('films', film_id)
            await self.redis.save_by_key(key, film)
        return Film(**film['_source']) if film else None

    async def get(self, sort: str, genre_id: str | None = None, page_number: int | None = 1, page_size: int | None = 10) -> list[Film]:
        key = make_redis_key('films', sort, genre_id, page_number, page_size)
        films = await self.redis.get_by_key(key)
        if not films:
            films = await self._get_films_from_elastic(sort=sort, genre_id=genre_id, page_number=page_number, page_size=page_size)
            await self.redis.save_by_key(key, films)
        return [Film(**doc['_source']) for doc in films['hits']['hits']]

    async def search(self, query: str, page_number: int | None = 1, page_size: int | None = 10) -> list[Film]:
        key = make_redis_key('films', query, page_number, page_size)
        films = await self.redis.get_by_key(key)
        if not films:
            films = await self._search_films_in_elastic(query, page_number=page_number, page_size=page_size)
            await self.redis.save_by_key(key, films)
        return [Film(**doc['_source']) for doc in films['hits']['hits']]

    async def _get_films_from_elastic(
        self, sort: str, genre_id: str | None = None, page_number: int | None = 1, page_size: int | None = 10
    ) -> dict:
        first_symbol = sort[0]
        if first_symbol.isalpha():
            sort_field = sort
            sort_order = 'asc'
        else:
            sort_field = sort[1:]
            sort_order = 'desc' if first_symbol == '-' else 'asc'

        body = {
            'sort': [{sort_field: sort_order}],
        }

        if genre_id:
            body |= {
                'query': {
                    'nested': {
                        'path': 'genres',
                        'query': {'term': {'genres.id': {'value': genre_id}}},
                    }
                },
            }
            
        return await self.elastic.search_by_query_with_pagination(index='films', body=body, page_number=page_number, page_size=page_size)

    async def _search_films_in_elastic(self, query: str, page_number: int | None = 1, page_size: int | None = 10) -> dict:
        return await self.elastic.search_by_query_with_pagination(
            index='films',
            body={
                'query': {
                    'multi_match': {
                        'query': query,
                        'fuzziness': 'auto',
                        'fields': [
                            'actors_names',
                            'writers_names',
                            'title',
                            'description',
                            'genres',
                        ],
                    }
                },
            },
            page_number=page_number,
            page_size=page_size,
        )


@lru_cache()
def get_film_service(
    redis: RedisClient = Depends(get_redis),
    elastic: ElasticClient = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic)
