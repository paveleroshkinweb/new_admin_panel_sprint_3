from db import PostgresDBRepository
from .etl_connections import get_pg_connection_manager, get_es_client_manager
from .etl_processor import ETLProcessor


def run_etl():
    with get_pg_connection_manager() as pgconnection, get_es_client_manager() as esclient:
        postgres_repository = PostgresDBRepository(pgconnection)
        etl_processor = ETLProcessor(sql_repository=postgres_repository, es_client=esclient)
        etl_processor.run()
