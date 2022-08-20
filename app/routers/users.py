from typing import List

from aioredis import Redis
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .. import schemas
from ..dependencies import get_current_user, get_session, get_redis_client
from ..services import users

from fastapi import BackgroundTasks

router = APIRouter(prefix='/users',
                   tags=['users'])


@router.get('/',
            response_model=List[schemas.User])
async def read_users(session: AsyncSession = Depends(get_session)):
    result = await users.get_users(session)
    return result


@router.post('/',
             response_model=schemas.User)
async def create_user(user: schemas.UserCreate, session: AsyncSession = Depends(get_session)):
    result = await users.create_user(session, user)
    return result


@router.post('/register',
             response_model=schemas.User)
async def register_user(user: schemas.UserCreate,
                        background_tasks: BackgroundTasks,
                        session: AsyncSession = Depends(get_session),
                        redis_client: Redis = Depends(get_redis_client)):
    result = await users.register_user(session, background_tasks, redis_client, user)
    return result


@router.get('/confirm',
            response_model=schemas.User)
async def confirm_email(code: str,
                        session: AsyncSession = Depends(get_session),
                        redis_client: Redis = Depends(get_redis_client)):
    result = await users.confirm_email(code, session, redis_client)
    return result


@router.post('/me',
             response_model=schemas.User)
async def get_current_user(user=Depends(get_current_user)):
    return user
