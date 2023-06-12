from abc import ABC, abstractmethod


class AsyncDataStorage(ABC):
    @abstractmethod
    async def get_by_id(self, index: str, _id: str) -> dict | None:
        pass

    @abstractmethod
    async def search_by_query_with_pagination(self, index: str, body: dict, page_number: int | None = 1, page_size: int | None = 10) -> dict:
        pass


class AsyncCacheStorage(ABC):
    @abstractmethod
    async def get_by_key(self, key) -> dict | list[dict]:
        pass

    @abstractmethod
    async def save_by_key(self, key, data):
        pass
