import asyncio
import time

from elasticsearch import Elasticsearch, NotFoundError

from settings import elastic_settings
from testdata.es_mapping import genres_settings, genres_mappings


def wait_es(es_client: Elasticsearch):
    while True:
        if es_client.ping():
            break
        time.sleep(1)
    return True

if __name__ == '__main__':
    elasticsearch_hosts = [f"http://{elastic_settings.ELASTIC_HOST}:{elastic_settings.ELASTIC_PORT}"]
    es_client = Elasticsearch(hosts=elasticsearch_hosts,
                                   verify_certs=False)
    init_result = wait_es(es_client)



