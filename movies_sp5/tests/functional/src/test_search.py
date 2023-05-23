import pytest


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'query': 'The Star'},
                {'status': 200, 'length': 10}
        ),
        (
                {'query': 'Mashed potato'},
                {'status': 200, 'length': 0}
        )
    ]
)
@pytest.mark.asyncio
async def test_search(query_data, expected_answer, es_data, es_write_data, make_get_request):   
    await es_write_data(es_data, 'movies', 'id') 

    status, body = await make_get_request('/films/search', query_data)

    assert status == expected_answer['status']
    assert len(body['items']) == expected_answer['length'], body
