from models.base import BaseOrjsonModel


class Person(BaseOrjsonModel):
    id: str
    name: str


class PersonFilmDetails(BaseOrjsonModel):
    id: str
    title: str
    imdb_rating: float


class PersonFilmDetailsRoles(BaseOrjsonModel):
    id: str
    roles: list[str]


class PersonFilm(BaseOrjsonModel):
    id: str
    full_name: str
    movies: list[PersonFilmDetailsRoles]
