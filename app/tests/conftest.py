import sys
import os
import pytest
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from app.models.db_models import Base
from app import settings

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

TEST_DATABASE_URL = settings.DATABASE_URL

@pytest.fixture(scope="session")
def event_loop():
    """Фикстура event_loop с session scope"""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def engine():
    """Асинхронный engine для тестов"""
    engine = create_async_engine(TEST_DATABASE_URL)
    yield engine
    await engine.dispose()

@pytest.fixture(scope="session", autouse=True)
async def prepare_db(engine):
    """Создает и очищает таблицы перед тестами"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def db_session(engine):
    """Асинхронная сессия для каждого теста"""
    async with AsyncSession(engine) as session:
        yield session
        await session.rollback()