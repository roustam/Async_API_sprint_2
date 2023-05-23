from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import Page
from pydantic import UUID4, BaseModel

from models.page import PageRequest
from api.v1.messages import GENRE_NOT_FOUND
from services.genre import GenreService, get_genre_service

router = APIRouter()


class Genre(BaseModel):
    uuid: UUID4
    name: str


@router.get("/", response_model=Page[Genre], summary='Get genres', description='Returns list of all genres')
async def genres(
    page_request: PageRequest = Depends(),
    genre_service: GenreService = Depends(get_genre_service),
):
    page, size = page_request.page, page_request.size
    page_of_genres, total = await genre_service.get_genres(page, size)

    return Page[Genre](
        items=[Genre(
            uuid=UUID(genre.id),
            name=genre.name
        )
            for genre in page_of_genres],
        page=page,
        size=size,
        total=total,
    )


@router.get("/{genre_id}", response_model=Genre, summary='Ger genre by id', description='Returns genre with specified id')
async def genre_name(
    genre_id: str, genre_service: GenreService = Depends(get_genre_service)
) -> Genre:
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=GENRE_NOT_FOUND)
    return Genre(uuid=UUID(genre.id), name=genre.name)
