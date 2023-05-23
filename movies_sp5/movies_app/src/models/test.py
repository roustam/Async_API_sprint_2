import asyncio

from elasticsearch import AsyncElasticsearch, NotFoundError

elastic = AsyncElasticsearch()


async def _search_films_in_elastic(query: str):
    res = await elastic.search(
        {
            "query": {
                "multi_match": {
                    "query": query,
                    "fuzziness": "auto",
                    "fields": ["id", "full_name", "movies"],
                }
            },
        },
        "persons",
    )

    return res["hits"]["hits"]


loop = asyncio.get_event_loop()
res = loop.run_until_complete(_search_films_in_elastic("Tom"))
loop.close()
print(res)

# curl -X POST -H "Content-Type: application/json" -d '{
#   "query": {
#     "multi_match": {
#       "query": "John",
#       "fields":["id","full_name"],
#     }
#   }
# }' http://localhost:9200/persons/_search
