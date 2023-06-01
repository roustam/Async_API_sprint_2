import random
import uuid

from faker import Faker

from .films import random_film, random_films

faker = Faker()


def random_id():
    return str(uuid.uuid4())


def random_person():
    return faker.name()


def random_roles(min: int = 1, max: int = 3):
    roles = [
        'actor',
        'director',
        'writer'
    ]
    num_roles = random.randint(min, max)
    selected_roles = random.sample(roles, num_roles)
    return selected_roles


def random_film():
    return {
        'id': random_id(),
        'roles': random_roles(1, 3)
    }


def random_films(min: int = 1, max: int = 5):
    return [random_film() for _ in range(random.randint(min, max))]


def random_person_record():
    return {
        'id': random_id(),
        'full_name': random_person(),
        'films': random_films(),
    }


def random_persons(qty: int):
    random_persons_list = [random_person_record() for _ in range(qty)]
    return random_persons_list
