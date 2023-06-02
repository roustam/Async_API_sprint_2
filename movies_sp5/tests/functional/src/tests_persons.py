import pytest

import random

from ..testdata.persons import random_films_extended, random_persons


def create_persons_list() -> list:
    persons = random_persons(qty=3)
    return persons


def choose_one_person(persons):
    person_to_request = random.choice(persons)
    return person_to_request


class TestPersons:
    @pytest.mark.asyncio
    async def test_person_by_id(self, es_write_persons, get_api_response):
        persons = create_persons_list()

        await es_write_persons(index='persons', data=persons, id='id')

        person_to_request = choose_one_person(persons)
        status, response_body = await get_api_response(
            f'/persons/{person_to_request["id"]}')

        person_to_request_movies = [
            {
                'uuid': film['id'],
                'roles': film['roles']
            } for film in person_to_request['films']
        ]

        assert status == 200
        assert response_body['uuid'] == person_to_request['id']
        assert response_body['full_name'] == person_to_request['full_name']
        assert response_body['films'] == person_to_request_movies

    @pytest.mark.asyncio
    async def test_all_films_by_person(self, es_write_person_movies, get_api_response):
        films = random_films_extended()
        person_to_request_id = '9758b894-57d7-465d-b657-c5803dd5b7f7'

        await es_write_person_movies(index='movies', data=films, id='id')

        status, response_body = await get_api_response(f'/persons/'
                                      f'{person_to_request_id}/film')

        expected_response = [
            {
                "uuid": "37c6cd37-1222-4470-9221-3170367d134b",
                "title": "Star Trek III: The Search for Spock",
                "imdb_rating": 6.7
            },
            {
                "uuid": "3d825f60-9fff-4dfe-b294-1a45fa1e115d",
                "title": "Star Wars: Episode IV - A New Hope",
                "imdb_rating": 8.6
            },
            {
                "uuid": "d1e24e68-1c00-4d81-8dff-9d126c1a6a5e",
                "title": "Star Trek: The Next Generation - A Final Unity",
                "imdb_rating": 7.9
            }
        ]

        assert status == 200
        assert response_body['items'] == expected_response
