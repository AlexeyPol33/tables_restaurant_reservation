from sqlalchemy.ext.asyncio import create_async_engine

host = '0.0.0.0'
port = 8000

#databases
DATABASE_URL = 'postgresql+asyncpg://postgres:postgres@localhost/tables_reservations'
engine = create_async_engine(DATABASE_URL)