from typing import Generic, TypeVar
from fastapi import APIRouter

from pydantic import BaseModel

from typing import Annotated

from fastapi import Query
from models.base import BaseOrjsonModel


router = APIRouter()


class PageRequest(BaseOrjsonModel):
    page_number: Annotated[int, Query(description='Pagination page number', ge=1)] = 1
    page_size: Annotated[int, Query(description='Pagination page size', ge=1)] = 10


T = TypeVar("T")


class Page(Generic[T], BaseModel):
    page: int
    size: int
    items: list[T]
