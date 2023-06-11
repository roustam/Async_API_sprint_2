from models.base import BaseOrjsonModel


class PersonFilmDetails(BaseOrjsonModel):
    id: str
    title: str
    imdb_rating: float


class PersonFilm(BaseOrjsonModel):
    id: str
    roles: list[str]


class Person(BaseOrjsonModel):
    id: str
    full_name: str
    films: list[PersonFilm]
