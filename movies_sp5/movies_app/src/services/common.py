from abc import ABC

from db.elastic import ElasticClient
from db.redis import RedisClient


def make_redis_key(entity: str, *args):
    return f'{entity}__' + '__'.join((str(arg) for arg in args))


class ServiceAbstract(ABC):
    def __init__(self, redis: RedisClient, elastic: ElasticClient):
        self.redis = redis
        self.elastic = elastic
