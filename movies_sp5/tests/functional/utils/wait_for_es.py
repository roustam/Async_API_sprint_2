import asyncio
import time

from elasticsearch import Elasticsearch, NotFoundError

from settings import elastic_settings

INDICES = {'genres':False,'films':False, 'persons': False}

def wait_es(es_client: Elasticsearch):
    # проверка на наличие индексов
    
    while True:
        if es_client.ping():
            if check_indices():
                break
        time.sleep(1)
    return True

def check_indices():
    for index_name in INDICES.keys():
        res = es_client.indices.exists(index=index_name)
        if res:
            INDICES[index_name] = True

    if [res for res in INDICES.values()] == [True,True,True]:
        return True
    else:
        return False


if __name__ == '__main__':
    elasticsearch_hosts = [f"http://{elastic_settings.ELASTIC_HOST}:{elastic_settings.ELASTIC_PORT}"]
    es_client = Elasticsearch(hosts=elasticsearch_hosts,
                                   verify_certs=False)
    init_result = wait_es(es_client)



