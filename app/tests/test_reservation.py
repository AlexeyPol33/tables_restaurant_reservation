import pytest
import asyncio
from datetime import datetime
from httpx import AsyncClient, ASGITransport
from app.main import app
from fastapi.testclient import TestClient


@pytest.fixture
def reservation():
    return {
        'customer_name': 'test_customer',
        'table_id': 1,
        'reservation_time': str(datetime.now()),
        'duration_minutes': 15
    }


@pytest.mark.asyncio
async def test_endpoint_ability(reservation):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response_get = asyncio.create_task(ac.get('/reservations/'))
        response_post = asyncio.create_task(ac.post('/reservations/',json=reservation))
        response_delete = asyncio.create_task(ac.delete('/reservations/1'))

        response_get, response_post, response_delete = await asyncio.gather(response_get, response_post, response_delete)
        assert response_get.status_code == 200
        assert response_post.status_code == 200
        assert response_delete.status_code == 200