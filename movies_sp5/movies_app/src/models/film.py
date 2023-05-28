from models.base import BaseOrjsonModel


class FilmGenre(BaseOrjsonModel):
    id: str
    name: str


class FilmPerson(BaseOrjsonModel):
    id: str
    name: str


class Film(BaseOrjsonModel):
    id: str
    imdb_rating: float
    genres: list[FilmGenre]
    title: str
    description: str | None
    directors_names: list[str]
    actors_names: list[str]
    writers_names: list[str]
    actors: list[FilmPerson]
    writers: list[FilmPerson]
    directors: list[FilmPerson]
