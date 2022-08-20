import secrets

from aioredis import Redis
from fastapi import BackgroundTasks, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, AsyncResult

from .. import models, schemas
from ..config import settings
from ..helpers import email
from ..logging import logger


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

    logger.info(f'{db_user} started registration process')

    code = secrets.token_urlsafe()
    await redis_client.set(code, db_user.id, ex=settings.token_ex)

    subject = 'Confirm your email'
    confirm_url = f'http://{settings.host}:{settings.port}/users/confirm?code={code}'
    message = f'Please confirm your email: {confirm_url}'

    background_tasks.add_task(email.send_email, user.email, subject, message)
    return db_user


async def confirm_email(code: str,
                        session: AsyncSession,
                        redis_client: Redis):
    user_id = await redis_client.get(code)

    if not user_id:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail='Code is invalid')

    result: AsyncResult = await session.execute(select(models.User).where(models.User.id == int(user_id)))
    user: models.User = result.scalars().first()

    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail='User does not exist')

    user.is_active = True
    await session.commit()
