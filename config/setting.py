from pydantic import BaseSettings
from functools import lru_cache


class Setting(BaseSettings):
    app_name: str = ''
    sqlalchemy_database_url: str = ""
    secret_key: str = ''
    algorithm: str = 'HS256'
    access_token_expire_minutes: int = 60

    class Config:
        env_file = '.env'


@lru_cache()
def get_settings():
    return Setting()
