from models.genre import Genre
from models.person import Person
from models.base import BaseOrjsonModel


class Film(BaseOrjsonModel):
    id: str
    imdb_rating: float
    genres: list[Genre]
    title: str
    description: str | None
    directors_names: list[str]
    actors_names: list[str]
    writers_names: list[str]
    actors: list[Person]
    writers: list[Person]
    directors: list[Person]
