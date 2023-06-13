import json
from typing import Iterable
from uuid import uuid4


def get_es_bulk_query(data: list[dict], index: str, id_field: str):
    bulk_query = []
    for row in data:
        bulk_query.extend([
            json.dumps({'index': {'_index': index, '_id': row[id_field]}}),
            json.dumps(row)
        ])
    return bulk_query


def prepare_bulk_data( index: str, data: list[dict]):
    bulk_data = []
    for record in data:
        bulk_data.append({"create": {"_index": index, "_id": record['id']}})
        bulk_data.append(record)
    return bulk_data


async def gen_bulk_data(index: str, records: list[dict]) -> Iterable[dict]:
    # helper that prepares data for async_bulk in es_write_data
    # not work(?)
    for record in records:
        yield {
            "_index": index,
            "_id": record['id'],
            "_source": record
        }

async def gen_bulk_data(records: list, index: str):
    for genre in records:
        record_uuid4 = uuid4()
        yield {
            "_index": index,
            "_id": record_uuid4,
            "_source": {"id": record_uuid4, 'name': genre},
        }


def persons_bulk_data(index: str, persons: list[dict], id_field: str):
    for person in persons:
        yield {
            '_index': index,
            '_id': person[id_field],
            "_source":{
                    'id': person['id'],
                    'full_name': person['full_name'],
                    'films': [
                        {
                            'id': film['id'],
                            'roles': film['roles']
                        } for film in person['films']
                    ]
            }
        }


def person_movies_bulk_data(index: str, movies: list[dict], id_field: str):
    for movie in movies:
        yield {
            '_index': index,
            '_id': movie[id_field],
            "_source":{
                    'id': movie['id'],
                    'imdb_rating': movie['imdb_rating'],
                    'genres': [
                        {
                            'id': genre['id'],
                            'name': genre['name']
                        } for genre in movie['genres']
                    ],
                    'title': movie['title'],
                    'description': movie['description'],
                    'directors_names': movie['directors_names'],
                    'actors_names': movie['actors_names'],
                    'writers_names': movie['writers_names'],
                    'actors':
                        [
                            {
                                'id': actor['id'],
                                'name': actor['name']
                            } for actor in movie['actors']
                        ],
                    'writers':
                        [
                            {
                                'id': writer['id'],
                                'name': writer['name']
                            } for writer in movie['writers']
                        ],
                    'directors':
                        [
                            {
                                'id': director['id'],
                                'name': director['name']
                            } for director in movie['directors']
                        ]
                    }
            }

# def make_bulk_data( index: str, data: list[dict],id_field: str):
#     bulk_data = []
#     for record in data:
#         bulk_data.append({"create": {"_index": index, "_id": record[id_field]}})
#         bulk_data.append({"_source": record})
#     return bulk_data


# async def gen_bulk_data(index: str, records: list[dict]):
#     # helper that prepares data for async_bulk in es_write_data
#     for record in records:
#         yield {
#             "_index": index,
#             "_id": record['id'],
#             "_source": record
#         }

