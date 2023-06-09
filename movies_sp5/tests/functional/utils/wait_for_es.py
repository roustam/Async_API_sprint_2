import asyncio
import time

from elasticsearch import Elasticsearch, NotFoundError

from settings import elastic_settings



def wait_es(es_client: Elasticsearch):
    # проверка на наличие индексов
    genres_index_exists = False
    films_index_exists = False
    persons_index_exists = False
    while True:
        if es_client.ping():
            genres_index_exists = es_client.indices.exists(index='genres')
            films_index_exists = es_client.indices.exists(index='films')
            persons_index_exists = es_client.indices.exists(index='persons')
            if genres_index_exists and films_index_exists and persons_index_exists:
                break
        time.sleep(1)
    return True

if __name__ == '__main__':
    elasticsearch_hosts = [f"http://{elastic_settings.ELASTIC_HOST}:{elastic_settings.ELASTIC_PORT}"]
    es_client = Elasticsearch(hosts=elasticsearch_hosts,
                                   verify_certs=False)
    init_result = wait_es(es_client)



