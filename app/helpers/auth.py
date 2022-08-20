import jwt

from ..config import settings


def create_access_token(sub, exp):
    encoded_jwt = jwt.encode({"sub": sub, "exp": exp}, settings.jwt_secret_key)
    return encoded_jwt
