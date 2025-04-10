import pytest
import asyncio
from datetime import datetime
from httpx import AsyncClient, ASGITransport
from app.main import app
from fastapi.testclient import TestClient


@pytest.fixture
def table():
    return {
        'name': 'Table 1',
        'seats': 3,
        'location': 'by the window'
    }


@pytest.mark.asyncio
async def test_endpoint_ability(table):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response_get = asyncio.create_task(ac.get('/tables/'))
        response_post = asyncio.create_task(ac.post('/tables/',json=table))
        response_delete = asyncio.create_task(ac.delete('/tables/1'))

        response_get, response_post, response_delete = await asyncio.gather(response_get, response_post, response_delete)
        assert response_get.status_code == 200
        assert response_post.status_code == 201
        assert response_delete.status_code == 200