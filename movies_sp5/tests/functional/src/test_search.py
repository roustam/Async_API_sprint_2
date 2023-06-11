import pytest
import random

@pytest.mark.parametrize(
    'query_data, expected_count',
    [
        ({'query': 'The Star'}, 10),
        ({'query': '$$$Tsts'}, 0),
    ]
)
@pytest.mark.asyncio
async def test_search(query_data, expected_count, search_film_data, 
                      es_write_data, make_get_request,flush_cache,clean_elasticsearch):   
    await clean_elasticsearch(index='films')
    await flush_cache()
    await es_write_data(index='films', data=search_film_data)

    body = await make_get_request('/films/search', query_data)
    redis_cache = await make_get_request('/films/search', query_data)

    assert body == redis_cache


    assert len(body['items']) == expected_count


@pytest.mark.asyncio
async def test_cleaning_films_data(make_get_request,flush_cache, clean_elasticsearch):
    await flush_cache()
    await clean_elasticsearch(index='films')
    body = await make_get_request('/films/search', {'query':'The star'})
    redis_cache = await make_get_request('/films/search', {'query':'$$$Test'})

    assert body == redis_cache
    assert body['items'] == []
    
