import random
import uuid

from faker import Faker

from .genres import GENRES


faker = Faker()


def random_id():
    return str(uuid.uuid4())


def random_rating():
    return round(random.uniform(0.0, 10.0), 1)


def random_title():
    return faker.text(max_nb_chars=20)


def random_description():
    return faker.sentence()


def random_genre():
    return {
        'id': random_id(),
        'name': random.choice(GENRES)
    }


def random_person():
    return {
        'id': random_id(),
        'name': faker.name()
    }


def random_genres(min: int = 1, max: int = 2):
    return [random_genre() for _ in range(random.randint(min, max))]


def random_persons(min: int = 1, max: int = 2):
    return [random_person() for _ in range(random.randint(min, max))]


def random_film():
    actors = random_persons(3, 5)
    writers = random_persons(1, 2)
    directors = random_persons(1, 2)
    return {
        'id': random_id(),
        'imdb_rating': random_rating(),
        'genres': random_genres(1, 3),
        'title': random_title(),
        'description': random_description(),
        'actors_names': [actor['name'] for actor in actors],
        'writers_names': [writer['name'] for writer in writers],
        'directors_names': [director['name'] for director in directors],
        'actors': actors,
        'writers': writers,
        'directors': directors,
    }


def random_films(qty: int):
    return [random_film() for _ in range(qty)]
