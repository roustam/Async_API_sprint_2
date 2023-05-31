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


# def make_bulk_data( index: str, data: list[dict],id_field: str):
#     bulk_data = []
#     for record in data:
#         bulk_data.append({"create": {"_index": index, "_id": record[id_field]}})
#         bulk_data.append({"_source": record})
#     return bulk_data


async def gen_bulk_data(records: list,index :str):
    for genre in records:
        record_uuid4 = uuid4()
        yield {
            "_index": index,
            "_id":record_uuid4,
            "_source": {"id": record_uuid4, 'name':genre},
        }