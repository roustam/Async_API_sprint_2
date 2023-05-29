from functools import lru_cache

import orjson
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from redis.asyncio import Redis

from db.elastic import get_elastic
from db.redis import get_redis
from models.person import Person, PersonFilmDetails
from services.common import make_redis_key, CACHE_EXPIRE_IN_SECONDS, ServiceAbstract


class PersonService(ServiceAbstract):
    async def get_by_id(self, person_id: str) -> Person | None:
        key = make_redis_key('person', person_id)
        person = await self._get_persons_from_cache(key)
        if not person:
            person = await self._get_person_from_elastic(person_id)
            if person:
                await self._save_persons_to_cache(key, person.body)
        return Person(**person['_source']) if person else None
    
    async def get_films_by_person_id(self, person_id: str, page_number: int | None = 1, page_size: int | None = 10) -> list[Person]:
        key = make_redis_key('person_films', person_id)
        person_films = await self._get_persons_from_cache(key)
        if not person_films:
            person_films = await self._search_person_films_in_elastic(person_id, page_number=page_number, page_size=page_size)
            await self._save_persons_to_cache(key, person_films.body)
        return [PersonFilmDetails(**doc['_source']) for doc in person_films['hits']['hits']]
    
    async def search(self, query: str, page_number: int | None = 1, page_size: int | None = 10) -> list[Person]:
        key = make_redis_key('persons', query, page_number, page_size)
        persons = await self._get_persons_from_cache(key)
        if not persons:
            persons = await self._search_persons_in_elastic(query, page_number=page_number, page_size=page_size)

            if persons['hits']['hits']:
                await self._save_persons_to_cache(key, persons.body)
        return [Person(**doc['_source']) for doc in persons['hits']['hits']]

    async def _get_persons_from_cache(self, key) -> dict | list[dict]:
        persons = await self.redis.get(key)
        return orjson.loads(persons) if persons else None
        
    async def _save_persons_to_cache(self, key, persons):
        await self.redis.set(key, orjson.dumps(persons).decode(), CACHE_EXPIRE_IN_SECONDS)

    async def _get_person_from_elastic(self, person_id: str) -> dict | None:
        try:
            return await self.elastic.get(index='persons', id=person_id)
        except NotFoundError:
            return None

    async def _search_person_films_in_elastic(self, person_id, page_number: int | None = 1, page_size: int | None = 10) -> dict:
        return await self.elastic.search(
            index='movies',
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
                'from': (page_number - 1) * page_size,
                'size': page_size,
            },
        )

    async def _search_persons_in_elastic(self, query: str, page_number: int | None = 1, page_size: int | None = 10) -> dict:
        return await self.elastic.search(
            index='persons',
            body={
                'query': {
                    'match': {
                        'full_name': query
                    }
                },
                'from': (page_number - 1) * page_size,
                'size': page_size,
            },
        )


@lru_cache()
def get_person_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(redis, elastic)
