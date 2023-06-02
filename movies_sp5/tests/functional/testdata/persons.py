import random
import uuid

from faker import Faker

from .genres import GENRES

faker = Faker()


def random_id():
    return str(uuid.uuid4())


def random_rating():
    return round(random.uniform(0.0, 10.0), 1)


def random_person():
    return faker.name()


def random_persons(qty: int):
    random_persons_list = [random_person_record() for _ in range(qty)]
    return random_persons_list


def random_roles(min: int = 1, max: int = 3):
    roles = [
        'actor',
        'director',
        'writer'
    ]
    num_roles = random.randint(min, max)
    selected_roles = random.sample(roles, num_roles)
    return selected_roles


def random_genre():
    return {
        'id': random_id(),
        'name': random.choice(GENRES)
    }


def random_genres(min: int = 1, max: int = 2):
    return [random_genre() for _ in range(random.randint(min, max))]


def random_title():
    return faker.text(max_nb_chars=20)


def random_description():
    return faker.sentence()


def random_film_shortened():
    return {
        'id': random_id(),
        'roles': random_roles(1, 3)
    }


def random_films_shortened(min: int = 1, max: int = 5):
    return [random_film_shortened() for _ in range(random.randint(min, max))]


def random_person_record():
    return {
        'id': random_id(),
        'full_name': random_person(),
        'films': random_films_shortened(),
    }


def random_films_extended():
    movies = [
        {
            "id": "37c6cd37-1222-4470-9221-3170367d134b",
            "imdb_rating": 6.7,
            "genres": [
                {
                    "id": "120a21cf-9097-479e-904a-13dd7198c1dd",
                    "name": "Adventure"
                },
                {
                    "id": "3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff",
                    "name": "Action"
                },
                {
                    "id": "6c162475-c7ed-4461-9184-001ef3d9f26e",
                    "name": "Sci-Fi"
                }],
            "title": "Star Trek III: The Search for Spock",
            "description": "Short description",
            "directors_names": [
            ],
            "actors_names": [
                "William Shatner",
            ],
            "writers_names": [
            ],
            "actors": [
                {
                    "id": "9758b894-57d7-465d-b657-c5803dd5b7f7",
                    "name": "William Shatner"
                },
            ],
            "writers": [
            ],
            "directors": [
            ]
        },
        {
            "id": "3d825f60-9fff-4dfe-b294-1a45fa1e115d",
            "imdb_rating": 8.6,
            "genres": [
                {
                    "id": "120a21cf-9097-479e-904a-13dd7198c1dd",
                    "name": "Adventure"
                },
                {
                    "id": "3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff",
                    "name": "Action"
                },
                {
                    "id": "b92ef010-5e4c-4fd0-99d6-41b6456272cd",
                    "name": "Fantasy"
                }],
            "title": "Star Wars: Episode IV - A New Hope",
            "description": "Short description",
            "directors_names": [
                "William Shatner",
            ],
            "actors_names": [
            ],
            "writers_names": [
                "George Lucas"
            ],
            "actors": [

            ],
            "writers": [
            ],
            "directors": [
                {
                    "id": "9758b894-57d7-465d-b657-c5803dd5b7f7",
                    "name": "William Shatner"
                },
            ]
        },
        {
            "id": "d1e24e68-1c00-4d81-8dff-9d126c1a6a5e",
            "imdb_rating": 7.9,
            "genres": [
                {
                    "id": "d1e24e68-1c00-4d81-8dff-9d126c1a6a5e",
                    "name": "Adventure"
                },
                {
                    "id": "3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff",
                    "name": "Action"
                },
                {
                    "id": "b92ef010-5e4c-4fd0-99d6-41b6456272cd",
                    "name": "Fantasy"
                }],
            "title": "Star Trek: The Next Generation - A Final Unity",
            "description": "Short description",
            "directors_names": [
                "William Shatner",
            ],
            "actors_names": [
                "Rafael Alencar",
            ],
            "writers_names": [
                "William Shatner"
            ],
            "actors": [
                {
                    "id": "0bd7752b-23c1-4a12-8f1a-ebd9e8b20216",
                    "name": "Rafael Alencar"
                }
            ],
            "writers": [
                {
                    "id": "9758b894-57d7-465d-b657-c5803dd5b7f7",
                    "name": "William Shatner"
                },
            ],
            "directors": [

            ]
        },
        {
            "id": "c60cb56f-eb05-45d2-be26-eacfd21c1d65",
            "imdb_rating": 8.0,
            "genres": [
                {
                    "id": "6c162475-c7ed-4461-9184-001ef3d9f26e",
                    "name": "Sci-Fi"
                }],
            "title": "Star Control",
            "description": "Short description",
            "directors_names": [
                "Paul Reiche III",
                "Fred Ford"
            ],
            "actors_names": [
                "Paul Reiche III"
            ],
            "writers_names": [
                "Fred Ford"
            ],
            "actors": [
                {
                    "id": "13f03554-78b0-4e1a-b16a-073c1502851e",
                    "name": "Paul Reiche III"
                }
            ],
            "writers": [
                {
                    "id": "91fbb296-fcc3-43fe-921d-6d016d08c9d0",
                    "name": "Fred Ford"
                },
            ],
            "directors": [
                {
                    "id": "13f03554-78b0-4e1a-b16a-073c1502851e",
                    "name": "Paul Reiche III"
                },
                {
                    "id": "91fbb296-fcc3-43fe-921d-6d016d08c9d0",
                    "name": "Fred Ford"
                }
            ]
        },

    ]
    return movies
