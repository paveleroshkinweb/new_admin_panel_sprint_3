from db import PostgresDBRepository
from settings import AppSettings
from state import RedisStateStorage
from .etl_connections import pg_connection_manager, get_es_handler, get_redis_client
from .etl_processor import ETLProcessor


app_settings = AppSettings()


def run_etl() -> None:
    with pg_connection_manager() as pgconnection:
        redis_client = get_redis_client()
        es_handler = get_es_handler()

        postgres_repository = PostgresDBRepository(pgconnection)
        state_storage = RedisStateStorage(redis_client=redis_client)
        etl_processor = ETLProcessor(
            sql_repository=postgres_repository,
            es_handler=es_handler,
            state_storage=state_storage,
            sleep_time=app_settings.sleep_seconds
        )
        etl_processor.run()
