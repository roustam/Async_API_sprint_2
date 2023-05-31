from elasticsearch import Elasticsearch, NotFoundError
import asyncio
import pytest
# from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk
from uuid import uuid4
# from functional.utils.helpers import make_bulk_data

ELASTIC_HOST='localhost'
ELASTIC_PORT='9200'

es = Elasticsearch(hosts=[f"http://{ELASTIC_HOST}:{ELASTIC_PORT}"],verify_certs=False)

try:
    res = es.indices.delete(index='genres')
    res = es.indices.delete(index='movies')
    res = es.indices.delete(index='persons')
    print('delete index',res)
except NotFoundError:
    print('index not found')
#
# genres_settings = {
#     "refresh_interval": "1s",
#     "analysis": {
#       "filter": {
#         "english_stop": {
#           "type":       "stop",
#           "stopwords":  "_english_"
#         },
#         "english_stemmer": {
#           "type": "stemmer",
#           "language": "english"
#         },
#         "english_possessive_stemmer": {
#           "type": "stemmer",
#           "language": "possessive_english"
#         },
#         "russian_stop": {
#           "type":       "stop",
#           "stopwords":  "_russian_"
#         },
#         "russian_stemmer": {
#           "type": "stemmer",
#           "language": "russian"
#         }
#       },
#       "analyzer": {
#         "ru_en": {
#           "tokenizer": "standard",
#           "filter": [
#             "lowercase",
#             "english_stop",
#             "english_stemmer",
#             "english_possessive_stemmer",
#             "russian_stop",
#             "russian_stemmer"
#           ]
#         }
#       }
#     }
#   }
# genres_mappings = {
#     "dynamic": "strict",
#     "properties": {
#       "id": {
#         "type": "keyword"
#       },
#       "name": {
#         "type": "text",
#         "fields": {
#           "raw": {
#             "type":  "keyword"
#           }
#         }
#       }
#     }
# }
#
# movies_settings = {
#   "refresh_interval": "1s",
#   "analysis": {
#     "filter": {
#       "english_stop": {
#         "type": "stop",
#         "stopwords": "_english_"
#       },
#       "english_stemmer": {
#         "type": "stemmer",
#         "language": "english"
#       },
#       "english_possessive_stemmer": {
#         "type": "stemmer",
#         "language": "possessive_english"
#       },
#       "russian_stop": {
#         "type": "stop",
#         "stopwords": "_russian_"
#       },
#       "russian_stemmer": {
#         "type": "stemmer",
#         "language": "russian"
#       }
#     },
#     "analyzer": {
#       "ru_en": {
#         "tokenizer": "standard",
#         "filter": [
#           "lowercase",
#           "english_stop",
#           "english_stemmer",
#           "english_possessive_stemmer",
#           "russian_stop",
#           "russian_stemmer"
#         ]
#       }
#     }
#   }
# }
# movies_mappings = {
#   "dynamic": "strict",
#   "properties": {
#     "id": {
#       "type": "keyword"
#     },
#     "imdb_rating": {
#       "type": "float"
#     },
#     "genres": {
#       "type": "nested",
#       "dynamic": "strict",
#       "properties": {
#         "id": {
#           "type": "keyword"
#         },
#         "name": {
#           "type": "keyword"
#         }
#       }
#     },
#     "title": {
#       "type": "text",
#       "analyzer": "ru_en",
#       "fields": {
#         "raw": {
#           "type": "keyword"
#         }
#       }
#     },
#     "description": {
#       "type": "text",
#       "analyzer": "ru_en"
#     },
#     "directors_names": {
#       "type": "text",
#       "analyzer": "ru_en"
#     },
#     "actors_names": {
#       "type": "text",
#       "analyzer": "ru_en"
#     },
#     "writers_names": {
#       "type": "text",
#       "analyzer": "ru_en"
#     },
#     "actors": {
#       "type": "nested",
#       "dynamic": "strict",
#       "properties": {
#         "id": {
#           "type": "keyword"
#         },
#         "name": {
#           "type": "text",
#           "analyzer": "ru_en"
#         }
#       }
#     },
#     "writers": {
#       "type": "nested",
#       "dynamic": "strict",
#       "properties": {
#         "id": {
#           "type": "keyword"
#         },
#         "name": {
#           "type": "text",
#           "analyzer": "ru_en"
#         }
#       }
#     },
#     "directors": {
#       "type": "nested",
#       "dynamic": "strict",
#       "properties": {
#         "id": {
#           "type": "keyword"
#         },
#         "name": {
#           "type": "text",
#           "analyzer": "ru_en"
#         }
#       }
#     }
#   }
# }
#
# persons_settings = {
#   "refresh_interval": "1s",
#   "analysis": {
#     "filter": {
#       "english_stop": {
#         "type": "stop",
#         "stopwords": "_english_"
#       },
#       "english_stemmer": {
#         "type": "stemmer",
#         "language": "english"
#       },
#       "english_possessive_stemmer": {
#         "type": "stemmer",
#         "language": "possessive_english"
#       },
#       "russian_stop": {
#         "type": "stop",
#         "stopwords": "_russian_"
#       },
#       "russian_stemmer": {
#         "type": "stemmer",
#         "language": "russian"
#       }
#     },
#     "analyzer": {
#       "ru_en": {
#         "tokenizer": "standard",
#         "filter": [
#           "lowercase",
#           "english_stop",
#           "english_stemmer",
#           "english_possessive_stemmer",
#           "russian_stop",
#           "russian_stemmer"
#         ]
#       }
#     }
#   }
# }
# persons_mappings = {
#   "dynamic": "strict",
#   "properties": {
#     "id": {
#       "type": "keyword"
#     },
#     "full_name": {
#       "type": "text",
#       "analyzer": "ru_en",
#       "fields": {
#         "raw": {
#           "type": "keyword"
#         }
#       }
#     },
#     "movies": {
#       "type": "nested",
#       "dynamic": "strict",
#       "properties": {
#         "id": {
#           "type": "keyword"
#         },
#         "roles": {
#           "type": "text",
#           "analyzer": "ru_en"
#         }
#       }
#     }
#   }
# }
#
# res = es.indices.create(index='genres', mappings=genres_mappings, settings=genres_settings)
# res = es.indices.create(index='movies', mappings=movies_mappings, settings=movies_settings)
# print(res)
# res = es.indices.create(index='persons', mappings=persons_mappings, settings=persons_settings)
# print(res)
#
# my_uuid=uuid4()
# res = es.create(index='genres',id=my_uuid, document={'id':my_uuid, 'name':'genre_name 1'})
