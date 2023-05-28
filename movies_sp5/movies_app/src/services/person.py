import json
from functools import lru_cache

import orjson
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from redis.asyncio import Redis

from db.elastic import get_elastic
from db.redis import get_redis
from models.person import PersonFilm, PersonFilmDetails, \
    PersonFilmDetailsRoles
from services.common import make_redis_key

person_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут


class PersonService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_by_id(self, person_id: str) -> PersonFilm | None:
        person = await self._person_from_cache(person_id)

        if not person:
            person = await self._get_person_from_elastic_by_id(person_id)

            if not person:
                return None
            await self._put_person_to_cache(person)

        return person

    async def _get_person_from_elastic_by_id(
        self, person_id: str
    ) -> PersonFilm | None:
        try:
            doc = await self.elastic.get(index="persons", id=str(person_id))
        except NotFoundError:
            return None
        return PersonFilm(**doc["_source"])

    async def _person_from_cache(self, person_id: str) -> PersonFilm | None:
        cache_key = make_redis_key('person', person_id)
        data = await self.redis.get(cache_key)
        if not data:
            return None

        return PersonFilm.parse_raw(data)

    async def _put_person_to_cache(self, person: PersonFilm):
        cache_key = make_redis_key('person', person.id)
        await self.redis.set(cache_key, person.json(),
                             person_CACHE_EXPIRE_IN_SECONDS)

    async def _get_film_for_person_from_cache(self, key):
        data = await self.redis.get(key)
        if data:
            return orjson.loads(data)
        else:
            return None

    async def _set_film_for_person_to_cache(self, key, data):
        data_json = orjson.dumps(data).decode()
        await self.redis.set(key, data_json, person_CACHE_EXPIRE_IN_SECONDS)

    async def _get_film_for_person_from_elastic(self, person_id) -> dict:
        try:
            result = await self.elastic.search(
                query = {
                    "query": {
                        "bool": {
                            "should": [
                                {
                                    "nested": {
                                        "path": "actors",
                                        "query": {
                                            "term": {"actors.id": person_id}},
                                    }
                                },
                                {
                                    "nested": {
                                        "path": "writers",
                                        "query": {
                                            "term": {"writers.id": person_id}},
                                    },
                                },
                                {
                                    "nested": {
                                        "path": "directors",
                                        "query": {"term": {
                                            "directors.id": person_id}},
                                    }
                                },
                            ]
                        }
                    }
                },
                index="movies",
            )
        except NotFoundError:
            return None

        return result

    async def get_film_for_person_by_id(self, person_id: str):
        redis_key = make_redis_key('person_details', person_id)
        res = await self._get_film_for_person_from_cache(redis_key)

        if not res:
            res = await self._get_film_for_person_from_elastic(person_id)
            await self._set_film_for_person_to_cache(redis_key, res)

        return [PersonFilmDetails(**doc["_source"]) for doc in
                res["hits"]["hits"]]

    async def _search_films_in_elastic(self, query: str) -> list:
        res = await self.elastic.search(
            {
                "query": {
                    "multi_match": {
                        "query": query,
                        "fuzziness": "auto",
                        "fields": ["id", "full_name", "movies"]
                    }
                },
            },
            "persons",
        )

        return res

    async def get_persons_with_films(self, query: str, page: int, size: int) \
            -> list[PersonFilm]:
        persons_with_films = await self._get_persons_with_films_from_cache(
            query, page, size
        )

        if persons_with_films is None:
            persons_with_films = await self._get_persons_with_films_from_elastic(
                query, page, size)

            if persons_with_films is None:
                return []

        await self._put_persons_with_films_to_cache(persons_with_films,
                                                    query, page, size)

        return persons_with_films

    async def _get_persons_with_films_from_cache(
        self, query: str, page: int, size: int
    ) -> list[PersonFilm] | None:
        cache_key = make_redis_key('persons', query, page, size)
        cached_persons_with_films = await self.redis.get(cache_key)

        if not cached_persons_with_films:
            return None

        deserialized_persons = json.loads(cached_persons_with_films)
        persons_with_films = [PersonFilm(**person) for person in
                              deserialized_persons]
        return persons_with_films

    async def _get_persons_with_films_from_elastic(self, query: str, page: int,
                                                   size: int) \
            -> list[PersonFilm]:
        es_query = {
            "query": {
                "match": {
                    "full_name": query
                }
            },
            "from": (page - 1) * size,
            "size": size,
        }

        result = await self.elastic.search(index="persons", body=es_query)

        persons_with_films = []
        for hit in result["hits"]["hits"]:
            person = hit["_source"]
            films = []
            for movie in person["movies"]:
                film = PersonFilmDetailsRoles(id=movie["id"],
                                              roles=movie["roles"])
                films.append(film)

            person_film = PersonFilm(id=person["id"],
                                     full_name=person["full_name"],
                                     movies=films)
            persons_with_films.append(person_film)
        return persons_with_films

    async def _put_persons_with_films_to_cache(
        self,
            persons_with_films: list[PersonFilm],
            query: str,
            page: int,
            size: int
    ) -> None:
        cache_key = make_redis_key('persons', query, page, size)
        serialized_persons = [person.dict() for person in persons_with_films]
        await self.redis.set(cache_key, json.dumps(serialized_persons),
                             ex=person_CACHE_EXPIRE_IN_SECONDS)


@lru_cache()
def get_person_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(redis, elastic)
