import os

from pydantic import BaseSettings


class AppSettings(BaseSettings):
    APP_HOST: str = os.getenv("APP_HOST", "127.0.0.1")
    APP_PORT: str = os.getenv("APP_PORT", 80)


class RedisSettings(BaseSettings):
    REDIS_HOST: str = os.getenv("REDIS_HOST", "127.0.0.1")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", 6379))


class ElasticSettings(BaseSettings):
    ELASTIC_HOST: str = os.getenv("ELASTIC_HOST", "127.0.0.1")
    ELASTIC_PORT: int = int(os.getenv("ELASTIC_PORT", 9200))
 

app_settings = AppSettings()
redis_settings = RedisSettings()
elastic_settings = ElasticSettings()
