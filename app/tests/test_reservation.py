import asyncio
import random
from typing import Sequence
from datetime import datetime, timedelta
from settings import engine
from models.db_models import Table, Reservation
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


async def create_reservation(customer_name, table_id, reservation_time, duration_minutes):
    async with AsyncSession(engine) as session:
        try:
            reservation = Reservation(
                customer_name=customer_name,
                table_id=table_id,
                reservation_time=reservation_time,
                duration_minutes=duration_minutes)
            session.add(reservation)
            await session.commit()
        except:
            pass

@pytest.fixture
async def reservations() -> Sequence[Reservation]:
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
    
    start_time = datetime.now()
    coro=[]
    for table in tables:
        table_id = table.id
        customer_name = f'custname_{table.id}'
        duration_minutes = random.randint(0, 1000)
        coro.append(asyncio.create_task(create_reservation(
            customer_name, table_id, start_time, duration_minutes
        )))
        start_time = start_time + timedelta(minutes=duration_minutes + 1)
    await asyncio.gather(*coro)
    async with AsyncSession(engine) as session:
        result = await session.execute(select(Reservation))
        reservations = result.scalars().all()
    return reservations


@pytest.mark.asyncio
async def test_list_reservations(reservations):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        request = await ac.get('/reservations/')
        reservations_count = len(reservations)
        request_reservations_count = len(request.json())
    
    assert request.status_code == 200
    assert reservations_count == request_reservations_count



@pytest.mark.asyncio
async def test_create_reservation(reservations):
    reservation = reservations[0]

    async with AsyncSession(engine) as session:
        await session.delete(reservation)
        await session.commit()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        request = await ac.post('/reservations/', json={
            "customer_name":reservation.customer_name,
            "table_id":reservation.table_id,
            "reservation_time":str(reservation.reservation_time),
            "duration_minutes":reservation.duration_minutes})
    assert request.status_code == 201


@pytest.mark.asyncio
async def test_create_reservation_conflict(reservations):
    reservation = reservations[1]

    async with AsyncSession(engine) as session:
        await session.delete(reservation)
        await session.commit()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        request = await ac.post('/reservations/', json={
            "customer_name":reservation.customer_name,
            "table_id":reservation.table_id,
            "reservation_time":str(reservation.reservation_time),
            "duration_minutes":reservation.duration_minutes + 100000})
    assert request.status_code == 400

@pytest.mark.asyncio
async def test_create_reservation_no_table(reservations):
    reservation = reservations[2]

    async with AsyncSession(engine) as session:
        await session.delete(reservation)
        table = await session.get(Table, reservation.table_id)
        await session.delete(table)
        await session.commit()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        request = await ac.post('/reservations/', json={
            "customer_name":reservation.customer_name,
            "table_id":reservation.table_id,
            "reservation_time":str(reservation.reservation_time),
            "duration_minutes":reservation.duration_minutes})
    assert request.status_code == 404

@pytest.mark.asyncio
async def test_delete_reservation(reservations):
    reservation = reservations[3]

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        request = await ac.delete(f'/reservations/{reservation.id}')
    assert request.status_code == 200