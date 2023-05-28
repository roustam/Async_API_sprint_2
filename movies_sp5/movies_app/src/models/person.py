from models.base import BaseOrjsonModel


class PersonFilmDetails(BaseOrjsonModel):
    id: str
    title: str
    imdb_rating: float


class PersonMovie(BaseOrjsonModel):
    id: str
    roles: list[str]


class Person(BaseOrjsonModel):
    id: str
    full_name: str
    movies: list[PersonMovie]
