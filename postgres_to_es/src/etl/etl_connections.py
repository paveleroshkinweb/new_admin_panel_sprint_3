from psycopg2.extras import DictCursor
from psycopg2.extensions import connection
from psycopg2 import connect as pgconnect, OperationalError
from elasticsearch import Elasticsearch
from redis import Redis
from redis.backoff import ExponentialBackoff
from redis.retry import Retry
from redis.exceptions import (
   BusyLoadingError,
   ConnectionError,
   TimeoutError
)

from contextlib import contextmanager, suppress
from typing import Generator
import logging

from settings import DatabaseSettings, ElasticSettings, RedisSettings
from es import ESHandler
from utils import backoff


logger = logging.getLogger(__name__)

db_settings = DatabaseSettings()
es_settings = ElasticSettings()
redis_settings = RedisSettings()

DSL = {
    'dbname': db_settings.name,
    'user': db_settings.user,
    'password': db_settings.password,
    'host': db_settings.host,
    'port': db_settings.port
}


@backoff(exceptions=(OperationalError,))
def get_pg_connection() -> connection:
    logger.debug("Obtaining postgres connection")
    pg_connection = pgconnect(**DSL, cursor_factory=DictCursor)
    return pg_connection


@contextmanager
def pg_connection_manager() -> Generator[connection, None, None]:
    pg_connection = None
    try:
        pg_connection = get_pg_connection()
        yield pg_connection
    finally:
        logger.debug("Closing postgres connection")
        # Ignore any error if by whatever reason connection can't be closed
        if not pg_connection:
            return
        with suppress(Exception):
            pg_connection.close()


def get_es_handler() -> ESHandler:
    logger.debug("Obtaining elasticsearch connection")
    client = Elasticsearch(
        f'http://{es_settings.host}:{es_settings.port}',
        retry_on_timeout=True,
        max_retries=4
    )
    es_handler = ESHandler(es_client=client, schema_path=es_settings.schema_path)
    return es_handler


def get_redis_client() -> Redis:
    logger.debug("Obtaining redis connection")
    redis_client = Redis(
        host=redis_settings.host,
        port=redis_settings.port,
        db=redis_settings.db,
        decode_responses=True,
        retry=Retry(ExponentialBackoff(), 3),
        retry_on_error=[BusyLoadingError, ConnectionError, TimeoutError]
    )
    redis_client.ping()
    return redis_client
