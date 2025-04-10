import asyncio
import random
from typing import Sequence
from settings import engine
from models.db_models import Table
from app.main import app

import pytest
from httpx import AsyncClient, ASGITransport
from fastapi.testclient import TestClient

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession


async def create_table(name, seats, location):
    async with AsyncSession(engine) as session:
        try:
            table = Table(name=name,seats=seats,location=location)
            session.add(table)
            await session.commit()
        except:
            pass


@pytest.fixture
async def tables() -> Sequence[Table]:
    coro = []
    for i in range(0,100):
        coro.append(asyncio.create_task(create_table(
            name=f'Table {i}',
            seats=random.randint(1,100),
            location=f'location {i}')))
    await asyncio.gather(*coro)
    async with AsyncSession(engine) as session:
        result = await session.execute(select(Table))
        tables = result.scalars().all()
    return tables


@pytest.mark.asyncio
async def test_list_tables(tables):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        request = await ac.get('/tables/')
        tables_count = len(tables)
        request_tables_count = len(request.json())

    assert request.status_code == 200
    assert tables_count == request_tables_count


@pytest.mark.asyncio
async def test_create_table(tables):
    table = tables[0]

    async with AsyncSession(engine) as session:
        await session.delete(table)
        await session.commit()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        request = await ac.post('/tables/', json={
            "name":table.name,
            "seats":table.seats,
            "location":table.location})
        assert request.status_code == 201

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        request = await ac.post('/tables/', json={
            "name":table.name,
            "seats":table.seats,
            "location":table.location})
        assert request.status_code == 400


@pytest.mark.asyncio
async def test_delete_table(tables):
    table = tables[1]
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        request = await ac.delete(f'/tables/{table.id}')
        assert request.status_code == 200