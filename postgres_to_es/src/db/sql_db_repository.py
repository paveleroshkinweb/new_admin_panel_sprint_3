from pydantic import BaseModel

from abc import ABC, abstractmethod
from typing import Iterable, Generator, Type, List, Dict


class SqlDBRepository(ABC):

    # SELECT_QUERY = 'SELECT {fields} FROM {table} {filter} {order};'

    # FIELDS_DELIMITER = ','

    @abstractmethod
    def execute_lazy_query(
        self,
        query: str,
        chunk_size: int = 1024
    ) -> Generator[List[Dict], None, None]:
        pass

    # @abstractmethod
    # def read_table(
    #         self,
    #         table_schema: Type[BaseModel],
    #         query: str,
    #         chunk_size: int = 1024) -> Generator[List[BaseModel], None, None]:
    #     pass

    # @staticmethod
    # def form_plain_select_query(
    #     fields: Iterable[str],
    #     table_name: str,
    #     schema_name: str = '',
    #     filter: str = '',
    #     order: str = ''
    # ) -> str:
    #     query_fields = SqlDBRepository.form_fields(fields)
    #     query_table_name = SqlDBRepository.form_table_name(table_name, schema_name)
    #     select_query = SqlDBRepository.SELECT_QUERY.format(
    #         fields=query_fields,
    #         table=query_table_name,
    #         filter=filter,
    #         order=order
    #     )
    #     return select_query

    # @staticmethod
    # def form_table_name(table: str, schema: str) -> str:
    #     if not schema:
    #         return table
    #     return f'{schema}.{table}'

    # @staticmethod
    # def form_fields(fields: Iterable[str]) -> str:
    #     return SqlDBRepository.FIELDS_DELIMITER.join(fields)
