from fastapi import HTTPException, Depends
from app.settings import engine
from app.models import db_models, schemas

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession


async def create_table(table: schemas.TableCreate):
    return {'method':'create_table'}


async def read_table(id: int):
    return {'method':'read_table'}


async def tables_list():

    return {'method':'tables_list'}


async def delete_table(id: int):
    return {'method':'delete_table'}


async def create_reservations(reservations: schemas.ReservationCreate):
    return {'method':'create_reservations'}


async def read_reservations(id: int):
    return {'method':'read_reservations'}


async def reservations_list():
    return {'method':'reservations_list'}


async def delete_reservations(id: int):
    return {'method':'delete_reservations'}