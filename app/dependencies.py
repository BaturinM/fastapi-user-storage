from aioredis import Redis
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, AsyncResult

from . import models
from .config import settings
from .database import SessionLocal

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


async def get_session():
    async with SessionLocal() as session:
        yield session


async def get_redis_client():
    async with Redis.from_url(settings.redis_url, decode_responses=True) as redis_client:
        yield redis_client


def get_bearer_token(token: str = Depends(oauth2_scheme)):
    return token


async def get_current_user(token: str = Depends(get_bearer_token),
                           session: AsyncSession = Depends(get_session),
                           redis_client: Redis = Depends(get_redis_client)):

    user_id = redis_client.get(token)
    if not user_id:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail='Invalid token')

    result: AsyncResult = await session.execute(select(models.User).where(models.User.id == user_id))
    user: models.User = result.scalars().first()
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail='User has been removed')
    return user
