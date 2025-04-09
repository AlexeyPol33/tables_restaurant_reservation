from fastapi import FastAPI

app = FastAPI()
DATABASE_URL = 'postgresql+asyncpg://postgres:postgres@localhost/tables_reservations'