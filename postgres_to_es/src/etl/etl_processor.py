from db import SqlDBRepository
from elasticsearch import Elasticsearch


class ETLProcessor:

    def __init__(self, sql_repository: SqlDBRepository, es_client: Elasticsearch) -> None:
        self.sql_repository = sql_repository
        self.es_client = es_client

    def run(self):
        print("HERE WE GO!")