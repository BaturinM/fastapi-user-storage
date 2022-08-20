from aioredis import Redis
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from .. import schemas
from ..dependencies import get_session, get_redis_client, get_bearer_token
from ..services import auth

security = HTTPBasic()

router = APIRouter(prefix='/auth',
                   tags=['auth'])


@router.post('/login',
             response_model=schemas.Token)
async def login_user(credentials: HTTPBasicCredentials = Depends(security),
                     session: AsyncSession = Depends(get_session),
                     redis_client: Redis = Depends(get_redis_client)):
    result = await auth.login_user(credentials, session, redis_client)
    return result


@router.get('/logout')
async def logout_user(token: str = Depends(get_bearer_token),
                      redis_client: Redis = Depends(get_redis_client)):
    result = await auth.logout_user(token, redis_client)
    return result
