from pydantic import BaseSettings
from functools import lru_cache


class Setting(BaseSettings):
    APP_NAME: str = ""
    SQLALCHEMY_DATABASE_URL: str = ""
    SECRET_KEY: str = ""
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Setting()
