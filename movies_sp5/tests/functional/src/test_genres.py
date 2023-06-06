import random
import time
import logging

import pytest
from testdata.genres import get_all_genres


class TestGenres:


    @pytest.mark.parametrize(
        'query_data, expected_answer',
        [
            (
                    {'page_number':1,'page_size':5},
                    {'length': 5}
            ),
            (
                    {'page_number': 2, 'page_size': 5},
                    {'length': 5}
            ),
            (
                    {'page_number': 1, 'page_size': 10},
                    {'length': 10}
            ),
            (
                    {'page_number': 1, 'page_size': 10},
                    {'length': 10}
            ),
        ]
    )
    @pytest.mark.asyncio
    async def test_genres(self, es_write_data,make_get_request, query_data,
                          expected_answer, get_genres):
        await es_write_data(index='genres', data=get_genres)
        body = await make_get_request('/genres', query_data)
        assert expected_answer['length'] == len(body['items'])

    @pytest.mark.asyncio
    async def test_genres_by_id(self, es_write_data, make_get_request,
                                get_genres, flush_cache, es_remove_data):

        await es_write_data(index='genres', data=get_genres)

        get_genres_length = len(get_genres)
        for genre_record in [get_genres[0], get_genres[-1], get_genres[get_genres_length // 2]]:
            redis_flush = await flush_cache()
            body_es = await make_get_request(f'/genres/{genre_record["id"]}')
            body_redis = await make_get_request(f'/genres/{genre_record["id"]}')

        #check for redis cache clearance
            assert redis_flush == True
        #testing for querying es
            assert body_es == body_redis

            print('es >>>>>', body_es)
            print('redis >>>>>', body_redis)


    # @pytest.mark.asyncio
    # async def test_genres_removal(self, make_get_request,
    #                             get_genres, flush_cache, es_remove_data):
    #     await flush_cache()
    #     await es_remove_data(index=['genres'])
    #
    #     body = await make_get_request('/genres', {"page_number": 1, 'page_size': 10})
    #     assert body['items'] == []
