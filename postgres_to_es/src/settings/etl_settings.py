from pydantic import BaseSettings, Field


PREFIX = 'ETL'


class LoggerSettings(BaseSettings):

    level: str

    class Config:
        env_prefix = f'{PREFIX}_LOG_'


class DatabaseSettings(BaseSettings):

    host: str

    port: int

    name: str

    user: str

    password: str

    class Config:
        env_prefix = f'{PREFIX}_DB_'


class ElasticSettings(BaseSettings):

    host: str

    port: int

    class Config:
        env_prefix = f'{PREFIX}_ES_'
