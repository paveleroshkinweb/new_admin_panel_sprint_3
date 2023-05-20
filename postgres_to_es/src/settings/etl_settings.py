from pydantic import BaseSettings


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

    schema_path: str

    movies_index_name: str

    movies_index_version: str

    class Config:
        env_prefix = f'{PREFIX}_ES_'


class RedisSettings(BaseSettings):

    host: str

    port: int

    db: int

    class Config:
        env_prefix = f'{PREFIX}_REDIS_'


class AppSettings(BaseSettings):

    sleep_seconds: int

    class Config:
        env_prefix = f'{PREFIX}_APP_'
