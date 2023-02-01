from pydantic import BaseSettings


class Settings(BaseSettings):
    host: str
    port: int
    sqlalchemy_database_url: str
    app_email: str
    redis_url: str
    token_ex: int
    smtp_host: str
    smtp_port: int
    jwt_secret_key: str

    class Config:
        env_file = ".env"


settings = Settings()
