from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import UUID4, BaseModel

from api.v1.messages import GENRE_NOT_FOUND
from api.v1.common import Page, Pagination

from services.genre import GenreService, get_genre_service


router = APIRouter()


class Genre(BaseModel):
    uuid: UUID4
    name: str


@router.get("/", response_model=Page[Genre], summary='Get genres', description='Returns list of all genres')
async def genres(
    pagination: Pagination = Depends(),
    genre_service: GenreService = Depends(get_genre_service),
):
    genres = await genre_service.get(page_number=pagination.page_number, page_size=pagination.page_size)

    return Page[Genre](
        items=[Genre(uuid=UUID(genre.id), name=genre.name) for genre in genres],
        page=pagination.page_number,
        size=pagination.page_size,
    )


@router.get("/{genre_id}", response_model=Genre, summary='Ger genre by id', description='Returns genre with specified id')
async def genre(
    genre_id: UUID4,
    genre_service: GenreService = Depends(get_genre_service),
):
    genre = await genre_service.get_by_id(genre_id)

    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=GENRE_NOT_FOUND)
    
    return Genre(uuid=UUID(genre.id), name=genre.name)
