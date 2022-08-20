from pydantic import BaseModel
from typing import Union


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: Union[None, str]


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str
