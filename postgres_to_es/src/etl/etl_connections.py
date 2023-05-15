from psycopg2.extras import DictCursor
from psycopg2.extensions import connection
from psycopg2 import connect as pgconnect
from elasticsearch import Elasticsearch

from contextlib import contextmanager
from typing import Generator
import logging

from settings import DatabaseSettings, ElasticSettings
from utils import backoff


logger = logging.getLogger(__name__)

db_settings = DatabaseSettings()
es_settings = ElasticSettings()

DSL = {
    'dbname': db_settings.name,
    'user': db_settings.user,
    'password': db_settings.password,
    'host': db_settings.host,
    'port': db_settings.port
}


@backoff(border_sleep_time=10)
def get_pg_connection() -> connection:
    logger.debug("Obtaining postgres connection")
    pg_connection = pgconnect(**DSL, cursor_factory=DictCursor)
    return pg_connection


@backoff(border_sleep_time=10)
def get_es_connection() -> Elasticsearch:
    logger.debug("Obtaining elasticsearch connection")
    client = Elasticsearch(
        f'http://{es_settings.host}:{es_settings.port}',
        retry_on_timeout=True,
        max_retries=5
    )
    return client


@contextmanager
def get_pg_connection_manager() -> Generator[connection, None, None]:
    pg_connection = None
    try:
        pg_connection = get_pg_connection()
        yield pg_connection
    finally:
        logger.debug("Closing postgres connection")
        if pg_connection:
            pg_connection.close()


@contextmanager
def get_es_client_manager() -> Generator[Elasticsearch, None, None]:
    es_client = None
    try:
        es_client = get_es_connection()
        yield es_client
    finally:
        logger.debug("Closing es connection")
        if es_client:
            es_client.transport.close()
