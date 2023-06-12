from functools import lru_cache

from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.person import Person, PersonFilmDetails
from db.abstract import AsyncDataStorage, AsyncCacheStorage
from services.common import make_redis_key, ServiceAbstract


class PersonService(ServiceAbstract):
    async def get_by_id(self, person_id: str) -> Person | None:
        key = make_redis_key('person', person_id)
        person = await self.redis.get_by_key(key)
        if not person:
            person = await self.elastic.get_by_id('persons', person_id)
            await self.redis.save_by_key(key, person)
        return Person(**person['_source']) if person else None
    
    async def get_films_by_person_id(self, person_id: str, page_number: int | None = 1, page_size: int | None = 10) -> list[Person]:
        key = make_redis_key('person_films', person_id)
        person_films = await self.redis.get_by_key(key)
        if not person_films:
            person_films = await self._search_person_films_in_elastic(person_id, page_number=page_number, page_size=page_size)
            await self.redis.save_by_key(key, person_films)
        return [PersonFilmDetails(**doc['_source']) for doc in person_films['hits']['hits']]
    
    async def search(self, query: str, page_number: int | None = 1, page_size: int | None = 10) -> list[Person]:
        key = make_redis_key('persons', query, page_number, page_size)
        persons = await self.redis.get_by_key(key)
        if not persons:
            persons = await self._search_persons_in_elastic(query, page_number=page_number, page_size=page_size)
            await self.redis.save_by_key(key, persons)
        return [Person(**doc['_source']) for doc in persons['hits']['hits']]

    async def _search_person_films_in_elastic(self, person_id, page_number: int | None = 1, page_size: int | None = 10) -> dict:
        return await self.elastic.search_by_query_with_pagination(
            index='films',
            body={
                'query': {
                    'bool': {
                        'should': [
                            {
                                'nested': {
                                    'path': 'actors',
                                    'query': {
                                        'term': {'actors.id': person_id}},
                                }
                            },
                            {
                                'nested': {
                                    'path': 'writers',
                                    'query': {
                                        'term': {'writers.id': person_id}},
                                },
                            },
                            {
                                'nested': {
                                    'path': 'directors',
                                    'query': {'term': {
                                        'directors.id': person_id}},
                                }
                            },
                        ]
                    }
                },
            },
            page_number=page_number,
            page_size=page_size,
        )

    async def _search_persons_in_elastic(self, query: str, page_number: int | None = 1, page_size: int | None = 10) -> dict:
        return await self.elastic.search_by_query_with_pagination(
            index='persons',
            body={
                'query': {
                    'match': {
                        'full_name': query
                    }
                },
            },
            page_number=page_number,
            page_size=page_size,
        )


@lru_cache()
def get_person_service(
        redis: AsyncCacheStorage = Depends(get_redis),
        elastic: AsyncDataStorage = Depends(get_elastic),
) -> PersonService:
    return PersonService(redis, elastic)
