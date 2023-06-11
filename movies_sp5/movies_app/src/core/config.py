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

    settings: dict = {
      'genres': {
        "refresh_interval": "1s",
        "analysis": {
          "filter": {
            "english_stop": {
              "type":       "stop",
              "stopwords":  "_english_"
            },
            "english_stemmer": {
              "type": "stemmer",
              "language": "english"
            },
            "english_possessive_stemmer": {
              "type": "stemmer",
              "language": "possessive_english"
            },
            "russian_stop": {
              "type":       "stop",
              "stopwords":  "_russian_"
            },
            "russian_stemmer": {
              "type": "stemmer",
              "language": "russian"
            }
          },
          "analyzer": {
            "ru_en": {
              "tokenizer": "standard",
              "filter": [
                "lowercase",
                "english_stop",
                "english_stemmer",
                "english_possessive_stemmer",
                "russian_stop",
                "russian_stemmer"
              ]
            }
          }
        }
      },
      'films': {
      "refresh_interval": "1s",
      "analysis": {
        "filter": {
          "english_stop": {
            "type": "stop",
            "stopwords": "_english_"
          },
          "english_stemmer": {
            "type": "stemmer",
            "language": "english"
          },
          "english_possessive_stemmer": {
            "type": "stemmer",
            "language": "possessive_english"
          },
          "russian_stop": {
            "type": "stop",
            "stopwords": "_russian_"
          },
          "russian_stemmer": {
            "type": "stemmer",
            "language": "russian"
          }
        },
        "analyzer": {
          "ru_en": {
            "tokenizer": "standard",
            "filter": [
              "lowercase",
              "english_stop",
              "english_stemmer",
              "english_possessive_stemmer",
              "russian_stop",
              "russian_stemmer"
            ]
          }
        }
      }
    },
      'persons': {
      "refresh_interval": "1s",
      "analysis": {
        "filter": {
          "english_stop": {
            "type": "stop",
            "stopwords": "_english_"
          },
          "english_stemmer": {
            "type": "stemmer",
            "language": "english"
          },
          "english_possessive_stemmer": {
            "type": "stemmer",
            "language": "possessive_english"
          },
          "russian_stop": {
            "type": "stop",
            "stopwords": "_russian_"
          },
          "russian_stemmer": {
            "type": "stemmer",
            "language": "russian"
          }
        },
        "analyzer": {
          "ru_en": {
            "tokenizer": "standard",
            "filter": [
              "lowercase",
              "english_stop",
              "english_stemmer",
              "english_possessive_stemmer",
              "russian_stop",
              "russian_stemmer"
            ]
          }
        }
      }
    }
    }

    mappings: dict = {
      'genres': {
          "dynamic": "strict",
          "properties": {
            "id": {
              "type": "keyword"
            },
            "name": {
              "type": "text",
              "fields": {
                "raw": {
                  "type":  "keyword"
                }
              }
            }
          }
      },
      'films': {
        "dynamic": "strict",
        "properties": {
          "id": {
            "type": "keyword"
          },
          "imdb_rating": {
            "type": "float"
          },
          "genres": {
            "type": "nested",
            "dynamic": "strict",
            "properties": {
              "id": {
                "type": "keyword"
              },
              "name": {
                "type": "keyword"
              }
            }
          },
          "title": {
            "type": "text",
            "analyzer": "ru_en",
            "fields": {
              "raw": {
                "type": "keyword"
              }
            }
          },
          "description": {
            "type": "text",
            "analyzer": "ru_en"
          },
          "directors_names": {
            "type": "text",
            "analyzer": "ru_en"
          },
          "actors_names": {
            "type": "text",
            "analyzer": "ru_en"
          },
          "writers_names": {
            "type": "text",
            "analyzer": "ru_en"
          },
          "actors": {
            "type": "nested",
            "dynamic": "strict",
            "properties": {
              "id": {
                "type": "keyword"
              },
              "name": {
                "type": "text",
                "analyzer": "ru_en"
              }
            }
          },
          "writers": {
            "type": "nested",
            "dynamic": "strict",
            "properties": {
              "id": {
                "type": "keyword"
              },
              "name": {
                "type": "text",
                "analyzer": "ru_en"
              }
            }
          },
          "directors": {
            "type": "nested",
            "dynamic": "strict",
            "properties": {
              "id": {
                "type": "keyword"
              },
              "name": {
                "type": "text",
                "analyzer": "ru_en"
              }
            }
          }
        }
      },
      'persons':{
        "dynamic": "strict",
        "properties": {
          "id": {
            "type": "keyword"
          },
          "full_name": {
            "type": "text",
            "analyzer": "ru_en",
            "fields": {
              "raw": {
                "type": "keyword"
              }
            }
          },
          "films": {
            "type": "nested",
            "dynamic": "strict",
            "properties": {
              "id": {
                "type": "keyword"
              },
              "roles": {
                "type": "text",
                "analyzer": "ru_en"
              }
            }
          }
        }
      },
    }





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
