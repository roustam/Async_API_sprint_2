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

def elastic_setup(es_client):
    print('setting up Elastic')
    result_idx_removal=''
    try:
        result_idx_removal = es_client.indices.delete(index='genres')
    except NotFoundError:
        print('Index not found')
    result_idx_creation = es_client.indices.create(index="genres",
                                           settings=genres_settings, mappings=genres_mappings)
    return {'Removal':result_idx_removal, "creation":result_idx_creation}


if __name__ == '__main__':
    elasticsearch_hosts = [f"http://{elastic_settings.ELASTIC_HOST}:{elastic_settings.ELASTIC_PORT}"]
    es_client = Elasticsearch(hosts=elasticsearch_hosts,
                                   verify_certs=False)
    init_result = wait_es(es_client)
    es_setup_result = elastic_setup(es_client)
    print('----init_result--->',init_result )


