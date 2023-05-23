import json


def get_es_bulk_query(data: list[dict], index: str, id_field: str):
    bulk_query = []
    for row in data:
        bulk_query.extend([
            json.dumps({'index': {'_index': index, '_id': row[id_field]}}),
            json.dumps(row)
        ])
    return bulk_query
