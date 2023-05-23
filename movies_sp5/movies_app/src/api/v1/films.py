from http import HTTPStatus
from typing import Annotated, Generic, TypeVar
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import UUID4, BaseModel
from api.v1.messages import FILM_NOT_FOUND

from services.film import FilmService, get_film_service


router = APIRouter()


T = TypeVar("T")


class Page(Generic[T], BaseModel):
    page: int
    size: int
    items: list[T]


class FilmGenre(BaseModel):
    uuid: UUID4
    name: str


class FilmPerson(BaseModel):
    uuid: UUID4
    full_name: str


class FilmDetails(BaseModel):
    uuid: UUID4
    title: str
    imdb_rating: float
    description: str | None
    genre: list[FilmGenre]
    actors: list[FilmPerson]
    writers: list[FilmPerson]
    directors: list[FilmPerson]


class Film(BaseModel):
    uuid: UUID4
    title: str
    imdb_rating: float


@router.get("/", response_model=Page[Film], summary='Get sorted films', description='Returns films sorted by specified key and filtered by genre')
async def films(
    sort: str = '-imdb_rating',
    genre: str | None = None,
    page_number: Annotated[int, Query(description='Pagination page number', ge=1)] = 1,
    page_size: Annotated[int, Query(description='Pagination page size', ge=1)] = 10,
    film_service: FilmService = Depends(get_film_service),
):
    """
    sort = 'imdb_rating' - asc sort
    sort = '-imdb_rating' - desc sort
    genre parameter takes genre id
    """
    films = await film_service.get(sort=sort, genre_id=genre, page_number=page_number, page_size=page_size)
    return Page(
        items=[
            Film(uuid=film.id, title=film.title, imdb_rating=film.imdb_rating)
            for film in films
        ],
        page=page_number,
        size=page_size,
    )


@router.get("/search", response_model=Page[Film], summary='Search films', description='Returns films according to query')
async def search_films(
    query: str,
    page_number: Annotated[int, Query(description='Pagination page number', ge=1)] = 1,
    page_size: Annotated[int, Query(description='Pagination page size', ge=1)] = 10,
    film_service: FilmService = Depends(get_film_service),
):
    """
    Search by query in films title, description, genres, person names
    """
    films = await film_service.search(query=query, page_number=page_number, page_size=page_size)
    return Page(
        items=[
            Film(uuid=film.id, title=film.title, imdb_rating=film.imdb_rating)
            for film in films
        ],
        page=page_number,
        size=page_size,
    )


@router.get("/{film_id}", response_model=FilmDetails, summary='Get film by id', description='Returns films with specified id')
async def film_details(
    film_id: UUID4,
    film_service: FilmService = Depends(get_film_service),
) -> FilmDetails:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=FILM_NOT_FOUND)

    return FilmDetails(
        uuid=UUID(film.id),
        title=film.title,
        imdb_rating=film.imdb_rating,
        description=film.description,
        genre=[FilmGenre(uuid=genre.id, name=genre.name) for genre in film.genres],
        actors=[
            FilmPerson(uuid=actor.id, full_name=actor.name) for actor in film.actors
        ],
        writers=[
            FilmPerson(uuid=writer.id, full_name=writer.name) for writer in film.writers
        ],
        directors=[
            FilmPerson(uuid=director.id, full_name=director.name)
            for director in film.directors
        ],
    )
