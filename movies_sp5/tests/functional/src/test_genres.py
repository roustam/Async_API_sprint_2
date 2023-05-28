import random
import pytest
from testdata.genres import get_all_genres

class TestGenres:

    @pytest.mark.asyncio
    async def test_genres(self, es_write_data, make_get_request):
        genres = get_all_genres()
        await es_write_data(genres, 'genres', 'id')
        body = await make_get_request('/genres',{'page':1, 'size':50})
        assert len(body['items']) == len(genres)
