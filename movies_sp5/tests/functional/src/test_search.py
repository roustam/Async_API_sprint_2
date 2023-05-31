import pytest


@pytest.mark.parametrize(
    'query_data, expected_count',
    [
        ({'query': 'The Star'}, 10),
        ({'query': 'Mashed potato'}, 0),
    ]
)
@pytest.mark.asyncio
async def test_search(query_data, expected_count, es_data, es_write_data, make_get_request):   
    # await es_write_data(es_data, 'movies', 'id')


    body = await make_get_request('/films/search', query_data)

    assert len(body['items']) == expected_count, body


