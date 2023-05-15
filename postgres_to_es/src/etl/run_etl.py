from psycopg2.extras import DictCursor
import psycopg2

from contextlib import contextmanager
import logging

from settings import DatabaseSettings, ElasticSettings
from db import PostgresDBRepository
from utils import backoff


logger = logging.getLogger(__name__)

db_settings = DatabaseSettings()

DSL = {
    'dbname': db_settings.name,
    'user': db_settings.user,
    'password': db_settings.password,
    'host': db_settings.host,
    'port': db_settings.port
}


@backoff(border_sleep_time=15)
def get_pg_connection():
    logger.debug("Obtaining postgres connection")
    pg_connection = psycopg2.connect(**DSL, cursor_factory=DictCursor)
    return pg_connection


@contextmanager
def get_pg_connection_manager():
    pg_conn = None
    try:
        pg_conn = get_pg_connection()
        yield pg_conn
    finally:
        logger.debug("Closing postgres connection")
        if pg_conn:
            pg_conn.close()


def run_etl():
    logger.debug("Running the etl")
