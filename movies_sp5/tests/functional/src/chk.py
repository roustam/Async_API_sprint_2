from elasticsearch import Elasticsearch
import json
from uuid import uuid4
import requests


ELASTIC_HOST='localhost'
ELASTIC_PORT='9200'

def es_client():
    client = Elasticsearch(
        hosts=[f"http://{ELASTIC_HOST}:{ELASTIC_PORT}"],
        verify_certs=False,
    )
    return client

es = es_client()
print('es client', es)
# query = json.dumps({"query": {"match_all": {}}})
res = es.delete_by_query(index='genres', query={"match_all":{}})
print(res)


# creating doc
# res = es.bulk(index='genres', query={"id":uuid4().__str__(), "name":"Comedy"})
# res = es.create(index='genres', id=uuid4(),  document={'id':uuid4(), 'name':'Cool Genre'})
# print(res,'<<<<<<<<,')
#

### bulk add

#
# def gendata():
#     mywords = ['foo', 'bar', 'baz']
#     for word in mywords:
#         yield {
#             "create":{
#                 "_id": uuid4(),
#                 'doc': {'name': word, 'id':uuid4()}
#             }
#         }
# genres = ["Action", "Comedy", "Drama"]
# ids = [1, 2, 3]
#
ops=[

    {"create" : { "_index" : "genres", "_id" : "141" }},
    {"index" : {  }},
    {"create" :{ "_index" : "genres", "_id" : "152" }},
    { "index" : {  }},
    {"create" :{ "_index" : "genres", "_id" : "165" }},

]



res = es.bulk(index="genres", operations=ops, refresh=True)
print('res', res)