from pydantic import BaseModel
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

import logging
from typing import List, Generator, Dict

# from psycopg2.extras import execute_batch

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

    # def read_table(
    #         self,
    #         table_schema: Type[BaseModel],
    #         query: str,
    #         chunk_size: int = 1024) -> Generator[List[BaseModel], None, None]:
    #     pass

    # def read_table(
    #         self,
    #         table_schema: Type[SqlBaseModel],
    #         chunk_size: int = 1024) -> Generator[List[SqlBaseModel], None, None]:
    #     raise NotImplementedError

    # def read_table_by_ids(
    #         self,
    #         table_schema: Type[SqlBaseModel],
    #         ids: List[str] = None,
    #         chunk_size: int = 1024) -> Generator[List[SqlBaseModel], None, None]:
    #     table = table_schema.get_meta_info().postgres_table_name
    #     schema = table_schema.get_meta_info().postgres_schema
    #     fields = list(table_schema.get_field_mapping().keys())
    #     with self.connection.cursor() as cursor:
    #         select_query = self.form_select_by_id_query(
    #             fields=fields,
    #             ids=ids,
    #             table_name=table,
    #             schema_name=schema
    #         )
    #         logger.info(READING_DATA_LOG.format(db=self.DB_NAME, table=table))

    #         cursor.execute(select_query)
    #         while True:
    #             data = cursor.fetchmany(chunk_size)
    #             logger.info(DATA_READ_LOG.format(db=self.DB_NAME, count=len(data), table=table))
    #             if data:
    #                 model_data = (self.update_model_names(dict(item), table_schema) for item in data)
    #                 yield [table_schema(**entry) for entry in model_data]
    #             else:
    #                 logger.info(NO_DATA_TO_READ_LOG.format(db=self.DB_NAME, table=table))
    #                 return

    # def write_table(self, data: List[SqlBaseModel]) -> None:
    #     if not data:
    #         logger.info(NO_DATA_LOG)
    #         return
    #     table = data[0].get_meta_info().postgres_table_name
    #     schema = data[0].get_meta_info().postgres_schema
    #     fields = list(data[0].get_field_mapping().keys())
    #     with self.connection.cursor() as cursor:
    #         query = self.form_insert_query(
    #             fields=fields,
    #             table_name=table,
    #             schema_name=schema
    #         )
    #         execute_batch(cursor, query, [self.extract_pg_values(fields, entry) for entry in data])
    #         self.connection.commit()

    #         logger.info(INSERTED_LOG.format(db=self.DB_NAME, count=len(data), table=table))

    # @staticmethod
    # def extract_pg_values(fields: Iterable[str], entry: SqlBaseModel) -> List[object]:
    #     pg_values = [getattr(entry, entry.FIELD_MAPPING[field]) for field in fields]
    #     return pg_values

    # @staticmethod
    # def update_model_names(data: Dict[str, object], table_schema: Type[SqlBaseModel]):
    #     new_data = {}
    #     field_mapping = table_schema.get_field_mapping()
    #     for key, value in data.items():
    #         new_data[field_mapping[key]] = value
    #     return new_data
