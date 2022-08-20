import asyncio

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app import app
from app import models
from app.database import Base
from app.dependencies import get_session

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./test.db"


engine = create_async_engine(SQLALCHEMY_DATABASE_URL,
                             connect_args={"check_same_thread": False})

TestingSessionLocal = sessionmaker(engine, class_=AsyncSession, autoflush=False)


async def init_db_data():
    async with TestingSessionLocal() as session:
        user = models.User(email='fake@test.com')
        session.add(user)
        await session.commit()


async def create_db():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    await init_db_data()


async def drop_db():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session")
def db_session():
    asyncio.run(create_db())
    yield
    asyncio.run(drop_db())


@pytest.fixture()
def client(db_session):
    async def override_get_session():
        async with TestingSessionLocal() as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session

    with TestClient(app) as client:
        yield client
