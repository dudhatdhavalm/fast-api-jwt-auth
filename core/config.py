from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    APP_NAME: str = 'userDb'
    SQLALCHEMY_DATABASE_URL: str = "postgresql://postgres:root@localhost/userDb"
    SECRET_KEY: str = '1f4cd5d9-504f-443e-9f85-181a1ed230d0'
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    class Config:
        case_sensitive = True
        env_file = '.env'


settings = Settings()
