import json
from uuid import uuid4


def get_es_bulk_query(data: list[dict], index: str, id_field: str):
    bulk_query = []
    for row in data:
        bulk_query.extend([
            json.dumps({'index': {'_index': index, '_id': row[id_field]}}),
            json.dumps(row)
        ])
    return bulk_query


async def gen_bulk_data(records: list,index :str):
    for genre in records:
        record_uuid4 = uuid4()
        yield {
            "_index": index,
            "_id":record_uuid4,
            "_source": {"id": record_uuid4, 'name':genre},
        }


def persons_bulk_data(index: str, persons: list, id_field: str):
    for person in persons:
        yield {
            '_index': index,
            '_id': person[id_field],
            "_source":{
                    'id': person['id'],
                    'full_name': person['full_name'],
                    'movies': [
                        {
                            'id': film['id'],
                            'roles': film['roles']
                        } for film in person['films']
                    ]
            }
        }
