import asyncio
import logging
import time
import traceback

from elasticsearch import Elasticsearch
from settings import elastic_settings

INDICES = {'genres':False,'films':False, 'persons': False}

def wait_es(es_client: Elasticsearch, 
            start_sleep_time=0.1, factor=2, border_sleep_time=25.0):
    n = 0
    t = start_sleep_time
    while True:
        try:
            if es_client.ping():
                if check_indices():
                    break
            elif border_sleep_time == t:
                logging.error(f'Elastics Search is unreachable after {n} attempts.')
                break
            else:
                t = start_sleep_time * (factor**n) if t < border_sleep_time else border_sleep_time
                n += 1
                logging.info(f'Trying to connect to Elastic search server.')
                time.sleep(t)
        except Exception as err:
            logging.error(err)
            logging.error(traceback.format_exc())


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



