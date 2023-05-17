from elasticsearch import Elasticsearch

from db import SqlDBRepository
from state import StateStorage


class ETLProcessor:

    def __init__(
            self,
            sql_repository: SqlDBRepository,
            es_client: Elasticsearch,
            state_storage: StateStorage) -> None:
        self.sql_repository = sql_repository
        self.es_client = es_client
        self.state_storage = state_storage

    def run(self):
        pass
