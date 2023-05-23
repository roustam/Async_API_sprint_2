from http import HTTPStatus
from typing import Generic, TypeVar, Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import UUID4, BaseModel
from api.v1.messages import PERSON_NOT_FOUND

from models.page import PageRequest
from services.person import PersonService, get_person_service

router = APIRouter()

T = TypeVar("T")


class Page(Generic[T], BaseModel):
    page: int
    size: int
    items: list[T]


class PersonDetailsFilm(BaseModel):
    id: UUID4
    roles: list[str]


class PersonDetails(BaseModel):
    uuid: UUID4
    full_name: str
    films: list[PersonDetailsFilm]


class PersonDetailsSearch(BaseModel):
    uuid: UUID4
    full_name: str
    movies: list[Any]


class FilmPerson(BaseModel):
    uuid: UUID4
    title: str
    imdb_dating: float


@router.get("/search", response_model=Page[PersonDetailsSearch],
            summary='Searching persons by string query',
            description='Returns persons with list of films in which '
                        'production they participated')
async def search_person_name(
        query: str,
        page_request: PageRequest = Depends(),
        person_service: PersonService = Depends(get_person_service)
):
    page, size = page_request.page, page_request.size
    set_of_person_films = await person_service.get_persons_with_films(
        query, page, size
    )
    return Page[PersonDetailsSearch](
        items=[
            PersonDetailsSearch(
                uuid=UUID4(person.id),
                full_name=person.full_name,
                movies=person.movies
            )
            for person in set_of_person_films
        ],
        page=page,
        size=size,
    )


@router.get(
    "/{person_id}",
    summary='Get person by id',
    description='Returns person with specified id'
)
async def person_details(
    person_id: UUID4,
    person_service: PersonService = Depends(get_person_service),
) -> PersonDetails:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=PERSON_NOT_FOUND)

    return PersonDetails(
        uuid=person.id, full_name=person.full_name, films=person.movies
    )


@router.get(
    "/{person_id}/film",
    summary='Get person\'s films',
    description='Returns films with specified person'
)
async def person_details_film(
    person_id: UUID4,
    person_service: PersonService = Depends(get_person_service),
):
    person_film = await person_service.get_film_for_person_by_id(person_id)

    return person_film
