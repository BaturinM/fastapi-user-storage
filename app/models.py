from passlib.apps import custom_app_context as pwd_context
from sqlalchemy import Boolean, Column, Integer, String

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    @property
    def password(self):
        return None

    @password.setter
    def password(self, password: str):
        self.hashed_password = pwd_context.hash(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.hashed_password)
