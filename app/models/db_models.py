from sqlalchemy import Column, Integer, BigInteger, \
ForeignKey, String, Double, DateTime, Text, Table, LargeBinary
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.ext.asyncio import create_async_engine


Base = declarative_base()

class Table(Base):
    __tablename__ = 'tables'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(25), unique=True)
    seats = Column(Integer)
    location = Column(Text)


class Reservation(Base):
    __tablename__ = 'reservations'
    id = Column(Integer, autoincrement=True, primary_key=True)
    customer_name = Column(Text)
    table_id = Column(Integer, ForeignKey('tables.id'))
    reservation_time = Column(DateTime)
    duration_minutes = Column(Integer)