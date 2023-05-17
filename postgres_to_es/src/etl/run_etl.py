from db import PostgresDBRepository
from state import RedisStateStorage
from .etl_connections import pg_connection_manager, get_es_client, get_redis_client
from .etl_processor import ETLProcessor


def run_etl() -> None:
    with pg_connection_manager() as pgconnection:
        redis_client = get_redis_client()
        es_client = get_es_client()

        postgres_repository = PostgresDBRepository(pgconnection)
        redis_state_storage = RedisStateStorage(redis_client=redis_client)
        etl_processor = ETLProcessor(sql_repository=postgres_repository, es_client=es_client, state_storage=redis_state_storage)
        etl_processor.run()
