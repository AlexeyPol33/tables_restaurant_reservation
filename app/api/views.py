from fastapi import HTTPException
from fastapi.responses import JSONResponse, Response
from settings import engine
from models import db_models, schemas

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


async def create_reservations(reservations: schemas.ReservationCreate):
    async with AsyncSession(engine) as session:
        pass
    return {'method':'create_reservations'}


async def reservations_list():
    async with AsyncSession(engine) as session:
        pass
    return {'method':'reservations_list'}


async def delete_reservations(id: int):
    async with AsyncSession(engine) as session:
        pass
    return {'method':'delete_reservations'}