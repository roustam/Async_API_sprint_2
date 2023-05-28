import logging

import fastapi.exceptions as fastapi_exceptions
import fastapi.exception_handlers as fastapi_exception_handlers
import gunicorn.app.base as gunicorn_app
import pydantic

from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis

from api.v1 import films, genres, persons
from core.config import ElasticSettings, RedisSettings, Settings
from db import elastic, redis


app = FastAPI(
    title="Read-only API для онлайн-кинотеатра",
    description="Информация о фильмах, жанрах и людях, "
                "участвовавших в создании произведения",
    version="1.0.0",
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.on_event("startup")
async def startup():
    redis_settings = RedisSettings()
    es_settings = ElasticSettings()
    redis.redis = Redis(host=redis_settings.REDIS_HOST, port=redis_settings.REDIS_PORT)
    elastic.es = AsyncElasticsearch(
        hosts=[f"http://{es_settings.ELASTIC_HOST}:{es_settings.ELASTIC_PORT}"]
    )


@app.on_event("shutdown")
async def shutdown():
    await redis.redis.close()
    await elastic.es.close()


class QueryParams(pydantic.BaseModel):
    test: int


@app.exception_handler(fastapi_exceptions.RequestValidationError)
async def validation_exception_handler(request, exc):
    logging.exception("RequestValidationError", exc_info=exc)
    return await fastapi_exception_handlers.request_validation_exception_handler(
        request, exc
    )


app.include_router(films.router, prefix="/api/v1/films", tags=["films"])
app.include_router(genres.router, prefix="/api/v1/genres", tags=["genres"])
app.include_router(persons.router, prefix="/api/v1/persons", tags=["persons"])

# add_pagination(app)


class Application(gunicorn_app.BaseApplication):
    def __init__(self, application, options):
        self.options = options
        self.application = application
        super().__init__()

    def load_config(self):
        config = {
            key: value
            for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


if __name__ == "__main__":
    app_settings = Settings()
    Application(app, options=app_settings.GUNICORN_OPTIONS).run()
