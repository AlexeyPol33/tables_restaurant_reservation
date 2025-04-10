from fastapi import HTTPException
from fastapi.responses import JSONResponse, Response
from settings import engine
from models import db_models, schemas
import datetime
import asyncio

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
import logging


logger = logging.getLogger(__name__)

async def create_table(table: schemas.TableCreate):
    async with AsyncSession(engine) as session:
        try:
            table = db_models.Table(**table.model_dump())
            session.add(table)
            await session.commit()
        except IntegrityError:
            return JSONResponse({'detail':'Error: The table name must be unique.'}, status_code=400)
        except Exception as _:
            logger.error(str(_))
            return JSONResponse('Unexpected error', status_code=500)

    return JSONResponse({'detail':'successfull'}, status_code=201)


async def tables_list():
    async with AsyncSession(engine) as session:
        result = await session.execute(select(db_models.Table))
        tables = result.scalars().all()

    tables = [schemas.Table.model_validate(table).model_dump() for table in tables]
    return JSONResponse(content=tables, status_code=200)


async def delete_table(id: int):
    async with AsyncSession(engine) as session:
        table = await session.get(db_models.Table, id)
        if table:
            await session.delete(table)
            await session.commit()
        else:
            return JSONResponse({'detail':'table not found'}, status_code=404)

    return JSONResponse({'detail':'successfull'},status_code=200)


async def create_reservations(request_reservation: schemas.ReservationCreate):
    async with AsyncSession(engine) as session:
        table = session.get(db_models.Table, request_reservation.table_id)
        reservations = session.execute(
                select(db_models.Reservation).where(
                    db_models.Reservation.table_id == request_reservation.table_id))
        try:
            reservation = db_models.Reservation(**request_reservation.model_dump())
        except Exception as _:
            logger.error(str(_))
            return JSONResponse('Unexpected error', status_code=500)
        
        #Если стол не существует
        table = await table
        if not table:
            return JSONResponse({'detail':'table not found'}, status_code=404)
        
        # Поиск конфликта брони
        reservations = await reservations
        request_reservation_start = request_reservation.reservation_time
        request_reservation_end = request_reservation_start + datetime.timedelta(minutes=request_reservation.duration_minutes)
        for res in reservations.scalars().all():
            res_start = res.reservation_time
            res_end = res_start + datetime.timedelta(minutes=res.duration_minutes)
            if request_reservation_start < res_start and request_reservation_end < res_end:
                continue
            if request_reservation_start > res_start and request_reservation_end > res_end:
                continue
            else:
                return JSONResponse({'detail':'An attempt to reservation within an existing time interval'}, status_code=400)

        session.add(reservation)
        await session.commit()

    return JSONResponse({'detail':'successfull'}, status_code=201)


async def reservations_list():
    async with AsyncSession(engine) as session:
        result = await session.execute(select(db_models.Reservation))
        reservations = result.scalars().all()
    response = []
    for reservation in  reservations:
        reservation = schemas.Reservation.model_validate(reservation).model_dump()
        reservation['reservation_time'] = str(reservation['reservation_time'])
        response.append(reservation)

    return JSONResponse(content=response, status_code=200)


async def delete_reservations(id: int):
    async with AsyncSession(engine) as session:
        reservation = await session.get(db_models.Reservation, id)
        if reservation:
            await session.delete(reservation) 
            await session.commit()
        else:
            return JSONResponse({'detail':'reservation not found'}, status_code=404)

    return JSONResponse({'detail':'successfull'},status_code=200)