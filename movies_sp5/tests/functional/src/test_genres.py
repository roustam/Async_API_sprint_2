import random
import time

import pytest

from testdata.genres import GENRES

class TestGenres:
    @pytest.mark.parametrize(
        'query_data, expected_answer',
        [
            (
                    {'page_number':1,'page_size':5},
                    {'length': 5}
            ),
            (
                    {'page_number': 1, 'page_size': 10},
                    {'length': 10}
            ),
        ]
    )
    @pytest.mark.asyncio
    async def test_genres(self, es_write_data, make_get_request, query_data, expected_answer):
        await es_write_data(index='genres', data=GENRES)
        body = await make_get_request('/genres', query_data)
        assert expected_answer['length'] == len(body['items'])


