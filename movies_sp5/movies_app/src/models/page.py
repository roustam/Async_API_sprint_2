from models.base import BaseOrjsonModel


class PageRequest(BaseOrjsonModel):
    page: int | None = 1
    size: int | None = 15
