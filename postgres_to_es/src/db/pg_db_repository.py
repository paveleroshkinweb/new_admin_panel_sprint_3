from psycopg2.extensions import connection as _connection

import logging
from typing import List, Generator, Dict

from .sql_db_repository import SqlDBRepository
from . import db_logs


logger = logging.getLogger(__name__)


class PostgresDBRepository(SqlDBRepository):

    DB_NAME = 'potgres'

    def __init__(self, pg_conn: _connection):
        self.connection = pg_conn

    def execute_lazy_query(
        self,
        query: str,
        chunk_size: int = 1024
    ) -> Generator[List[Dict], None, None]:
        with self.connection.cursor() as cursor:
            logger.info(db_logs.EXECUTING_QUERY_LOG.format(query=query))
            cursor.execute(query)
            self.connection.commit()
            while True:
                data = cursor.fetchmany(chunk_size)
                if data:
                    yield [dict(item) for item in data]
                else:
                    return
