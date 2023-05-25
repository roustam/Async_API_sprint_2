from http import HTTPStatus
from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, Query
from pydantic import UUID4, BaseModel

from api.v1.messages import GENRE_NOT_FOUND
from api.v1.common import Page, router

from services.genre import GenreService, get_genre_service


class Genre(BaseModel):
    uuid: UUID4
    name: str


@router.get("/", response_model=Page[Genre], summary='Get genres', description='Returns list of all genres')
async def genres(
    page_number: Annotated[int, Query(description='Pagination page number', ge=1)] = 1,
    page_size: Annotated[int, Query(description='Pagination page size', ge=1)] = 10,
    genre_service: GenreService = Depends(get_genre_service),
):
    genres = await genre_service.get(page_number=page_number, page_size=page_size)

    return Page[Genre](
        items=[Genre(uuid=UUID(genre.id), name=genre.name) for genre in genres],
        page=page_number,
        size=page_size,
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
