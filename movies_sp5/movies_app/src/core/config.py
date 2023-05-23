import os

from pydantic import BaseSettings, Field

from core.logger import LOGGING


class RedisSettings(BaseSettings):
    # Настройки Redis
    REDIS_HOST: str = os.getenv("REDIS_HOST", "127.0.0.1")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", 6379))


class ElasticSettings(BaseSettings):
    # Настройки Elasticsearch
    ELASTIC_HOST: str = os.getenv("ELASTIC_HOST", "127.0.0.1")
    ELASTIC_PORT: int = int(os.getenv("ELASTIC_PORT", 9200))


class Settings(BaseSettings):
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "movies")

    # Корень проекта
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Применяем настройки логирования
    LOGGING_CONF: dict = LOGGING

    # Настройки Gunicorn
    gunicorn_host: str = "0.0.0.0"
    gunicorn_port: str = "80"
    worker_class: str = "uvicorn.workers.UvicornWorker"
    GUNICORN_OPTIONS: dict = {
        "bind": "%s:%s" % (gunicorn_host, gunicorn_port),
        "workers": 4,
        "worker_class": worker_class,
        "log_config": LOGGING,
    }

    # Настройки логирования
    LOGGING_CONF: dict = LOGGING
