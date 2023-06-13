from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import UUID4, BaseModel
from api.v1.messages import PERSON_NOT_FOUND

from api.v1.common import Page, Pagination

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
    pagination: Pagination = Depends(),
    person_service: PersonService = Depends(get_person_service),
):
    persons = await person_service.search(query, page_number=pagination.page_number, page_size=pagination.page_size)

    return Page[Person](
        items=[
            Person(
                uuid=UUID(person.id),
                full_name=person.full_name,
                films=[
                    PersonFilm(uuid=UUID(film.id), roles=film.roles)
                    for film in person.films
                ],
            )
            for person in persons
        ],
        page=pagination.page_number,
        size=pagination.page_size,
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
            PersonFilm(uuid=UUID(film.id), roles=film.roles)
            for film in person.films
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
    pagination: Pagination = Depends(),
    person_service: PersonService = Depends(get_person_service),
):
    films = await person_service.get_films_by_person_id(person_id, page_number=pagination.page_number, page_size=pagination.page_size)

    return Page[PersonFilmDetails](
        items=[
            PersonFilmDetails(
                uuid=UUID(film.id),
                title=film.title,
                imdb_rating=film.imdb_rating,
            )
            for film in films
        ],
        page=pagination.page_number,
        size=pagination.page_size,
    )
