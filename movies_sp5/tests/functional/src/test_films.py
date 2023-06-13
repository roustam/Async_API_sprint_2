import random

import pytest
from testdata.films import random_films


class TestFilms:
    @pytest.mark.parametrize(
        'query_data, order',
        [
            ({'sort': '-imdb_rating'}, 'desc'),
            ({'sort': 'imdb_rating'}, 'asc'),
        ] 
    )
    @pytest.mark.asyncio
    async def test_films_sorted(self, es_write_data, make_get_request,flush_cache,
                                query_data, order,get_films, clean_elasticsearch):
        await flush_cache()
        await clean_elasticsearch(index='films')
        await es_write_data(index='films', data=get_films)

        body = await make_get_request('/films', query_data)
        redis_cache = await make_get_request('/films', query_data)

        assert body == redis_cache
        assert len(body['items']) == len(get_films)
        assert body['items'] == [
            {'uuid': film['id'], 'title': film['title'], 'imdb_rating': film['imdb_rating']}
            for film
            in sorted(get_films, key=lambda film: film['imdb_rating'], reverse=order=='desc')
        ]

    @pytest.mark.asyncio
    async def test_films_filtered(self, es_write_data, make_get_request, get_films,
                                  flush_cache,clean_elasticsearch):
        await flush_cache()
        await clean_elasticsearch(index='films')
        await es_write_data(index='films',data=get_films)

        film_for_filtering = random.choice(get_films)
        body = await make_get_request('/films', {'sort': '-imdb_rating',
                                                 'genre': random.choice(film_for_filtering['genres'])['id']})

        assert body['items'] == [{'uuid': film_for_filtering['id'], 'title': film_for_filtering['title'],
                                  'imdb_rating': film_for_filtering['imdb_rating']}]

    @pytest.mark.asyncio
    async def test_film_by_id(self, es_write_data, make_get_request, get_films,
                              flush_cache,clean_elasticsearch):
        await flush_cache()
        await clean_elasticsearch(index='films')
        await es_write_data(index='films', data=get_films)

        film_for_get = random.choice(get_films)
        body = await make_get_request(f'/films/{film_for_get["id"]}')

        assert body == {
            'uuid': film_for_get['id'],
            'title': film_for_get['title'],
            'imdb_rating': film_for_get['imdb_rating'],
            'description': film_for_get['description'],
            'genre': [
                {
                    'uuid': genre['id'],
                    'name': genre['name']
                } for genre in film_for_get['genres']
            ],
            'actors': [
                {
                    'uuid': actor['id'],
                    'full_name': actor['name']
                } for actor in film_for_get['actors']
            ],
            'writers': [
                {
                    'uuid': writer['id'],
                    'full_name': writer['name']
                } for writer in film_for_get['writers']
            ],
            'directors': [
                {
                    'uuid': director['id'],
                    'full_name': director['name']
                } for director in film_for_get['directors']
            ],
        }
