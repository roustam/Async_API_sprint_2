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
            )
        ]
    )
    @pytest.mark.asyncio
    async def test_genres(self, es_write_data,make_get_request, query_data,
                          expected_answer, get_genres, flush_cache):
        await flush_cache()
        await es_write_data(index='genres', data=get_genres)
        body = await make_get_request('/genres', query_data)

        cached_body = await make_get_request('/genres', query_data)
        assert body['items'] == cached_body['items']
        genre_items = [{'uuid':genre['id'], 'name':genre['name']} for genre in get_genres]
        print('--->', genre_items[:(query_data['page_number'] * query_data['page_size'])])

        assert body['items'] == genre_items[
            query_data['page_number'] * query_data['page_size'] - query_data['page_size']
            :query_data['page_number'] * query_data['page_size']]


    @pytest.mark.asyncio
    async def test_genres_by_id(self, es_write_data, make_get_request,
                                get_genres, flush_cache, es_remove_data):
        await flush_cache()
        await es_write_data(index='genres', data=get_genres)

        get_genres_length = len(get_genres)
        for genre_record in [get_genres[0], get_genres[-1], get_genres[get_genres_length // 2]]:
            request_url = f'/genres/{genre_record["id"]}'
            body_es = await make_get_request(request_url)
            body_redis = await make_get_request(request_url)

            #testing for querying es

            assert body_es == {'name':genre_record['name'], 'uuid':genre_record['id']}
            assert body_redis == {'name':genre_record['name'], 'uuid':genre_record['id']}

        redis_flush = await flush_cache()
        assert redis_flush == True
