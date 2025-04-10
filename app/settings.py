from sqlalchemy.ext.asyncio import create_async_engine
from os import getenv
from dotenv import load_dotenv


load_dotenv()

host = getenv('HOST','0.0.0.0')
port = getenv('PORT',8000)

DEBUG = getenv('DEBUG', False)

#databases
DB_NAME = getenv('DB_NAME','tables_reservations')
DB_USER = getenv('DB_USER','postgres')
DB_PASSWORD = getenv('DB_PASSWORD','postgres')
DB_HOST =  getenv('DB_HOST','localhost')
DB_PORT = getenv('DB_PORT','5432')

DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
engine = create_async_engine(DATABASE_URL)