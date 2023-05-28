from http import HTTPStatus
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import UUID4, BaseModel
from api.v1.messages import PERSON_NOT_FOUND

from api.v1.common import Page

from services.person import PersonService, get_person_service


router = APIRouter()


class PersonFilm(BaseModel):
    uuid: UUID4
    roles: list[str]


class Person(BaseModel):
    uuid: UUID4
    full_name: str
    films: list[PersonFilm]


class PersonFilmDetails(BaseModel):
    uuid: UUID4
    title: str
    imdb_rating: float


@router.get(
    "/search",
    response_model=Page[Person],
    summary='Searching persons by string query',
    description='Returns persons with list of films in which production they participated'
)
async def search_persons(
    query: str,
    page_number: Annotated[int, Query(description='Pagination page number', ge=1)] = 1,
    page_size: Annotated[int, Query(description='Pagination page size', ge=1)] = 10,
    person_service: PersonService = Depends(get_person_service),
):
    persons = await person_service.search(query, page_number=page_number, page_size=page_size)

    return Page[Person](
        items=[
            Person(
                uuid=UUID(person.id),
                full_name=person.full_name,
                films=[
                    PersonFilm(uuid=UUID(movie.id), roles=movie.roles)
                    for movie in person.movies
                ],
            )
            for person in persons
        ],
        page=page_number,
        size=page_size,
    )


@router.get(
    "/{person_id}",
    response_model=Person,
    summary='Get person by id',
    description='Returns person with specified id',
)
async def person(
    person_id: UUID4,
    person_service: PersonService = Depends(get_person_service),
):
    person = await person_service.get_by_id(person_id)

    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=PERSON_NOT_FOUND)

    return Person(
        uuid=UUID(person.id),
        full_name=person.full_name,
        films=[
            PersonFilm(uuid=UUID(movie.id), roles=movie.roles)
            for movie in person.movies
        ],
    )


@router.get(
    "/{person_id}/film",
    response_model=Page[PersonFilmDetails],
    summary='Get person\'s films',
    description='Returns films with specified person',
)
async def person_films_details(
    person_id: UUID4,
    page_number: Annotated[int, Query(description='Pagination page number', ge=1)] = 1,
    page_size: Annotated[int, Query(description='Pagination page size', ge=1)] = 10,
    person_service: PersonService = Depends(get_person_service),
):
    films = await person_service.get_films_by_person_id(person_id, page_number=page_number, page_size=page_size)

    return Page[PersonFilmDetails](
        items=[
            PersonFilmDetails(
                uuid=UUID(film.id),
                title=film.title,
                imdb_rating=film.imdb_rating,
            )
            for film in films
        ],
        page=page_number,
        size=page_size,
    )
