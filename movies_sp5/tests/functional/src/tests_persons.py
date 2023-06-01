import pytest

import random

from ..testdata.persons import random_persons


def create_persons_list() -> list:
    persons = random_persons(qty=3)
    return persons


def choose_one_person(persons):
    person_to_request = random.choice(persons)
    return person_to_request


class TestPersons:
    @pytest.mark.asyncio
    async def test_person_by_id(self, es_write_persons, make_get_request):
        persons = create_persons_list()

        await es_write_persons(index='persons', data=persons, id='id')

        person_to_request = choose_one_person(persons)
        response = await make_get_request(f'/persons/{person_to_request["id"]}')

        person_to_request_movies = [
            {
                'uuid': film['id'],
                'roles': film['roles']
            } for film in person_to_request['films']
        ]

        assert response['uuid'] == person_to_request['id']
        assert response['full_name'] == person_to_request['full_name']
        assert response['films'] == person_to_request_movies
