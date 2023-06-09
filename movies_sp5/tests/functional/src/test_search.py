import pytest


@pytest.mark.parametrize(
    'query_data, expected_count',
    [
        ({'query': 'The Star'}, 10),
        ({'query': '$$$Tsts'}, 0),
    ]
)
@pytest.mark.asyncio
async def test_search(query_data, expected_count, search_film_data, 
                      es_write_data, make_get_request,flush_cache):   
    
    await flush_cache()
    await es_write_data(index='films', data=search_film_data)

    body = await make_get_request('/films/search', query_data)
    redis_cache = await make_get_request('/films/search', query_data)

    assert body == redis_cache


    assert len(body['items']) == expected_count


