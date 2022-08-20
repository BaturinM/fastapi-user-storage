import secrets

from aioredis import Redis
from fastapi import BackgroundTasks
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, AsyncResult

from .. import models, schemas
from ..config import settings
from ..helpers import email


async def get_users(session: AsyncSession):
    result: AsyncResult = await session.execute(select(models.User))
    return result.scalars().all()


async def create_user(session: AsyncSession, user: schemas.UserCreate):
    db_user = models.User(email=user.email, password=user.password)
    session.add(db_user)
    await session.commit()
    return db_user


async def register_user(session: AsyncSession,
                        background_tasks: BackgroundTasks,
                        redis_client: Redis,
                        user: schemas.UserCreate):

    db_user = models.User(email=user.email, password=user.password, is_active=False)
    session.add(db_user)
    await session.commit()

    code = secrets.token_urlsafe()

    await redis_client.set(code, db_user.id, ex=settings.token_ex)

    subject = "Registration"
    message = f"Your registration code: {code}"

    background_tasks.add_task(email.send_email, user.email, subject, message)
    return db_user
