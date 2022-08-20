from datetime import datetime, timedelta

from aioredis import Redis
from fastapi import HTTPException, status
from fastapi.security import HTTPBasicCredentials
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, AsyncResult

from .. import models
from ..config import settings
from ..helpers.auth import create_access_token
from ..logging import logger


async def login_user(credentials: HTTPBasicCredentials, session: AsyncSession, redis_client: Redis):
    logger.debug(credentials)
    result: AsyncResult = await session.execute(select(models.User).where(models.User.email == credentials.username))
    user: models.User = result.scalars().first()

    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail='User does not exist')
    if not user.is_active:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail='User is not active')

    if not user.verify_password(credentials.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect password')

    access_token = create_access_token(user.id, datetime.utcnow() + timedelta(seconds=settings.token_ex))
    await redis_client.set(access_token, user.id, ex=settings.token_ex)
    return {'access_token': access_token, 'token_type': 'bearer'}


async def logout_user(token: str, redis_client: Redis):
    await redis_client.delete(token)
