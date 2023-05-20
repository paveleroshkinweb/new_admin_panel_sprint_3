from elasticsearch import Elasticsearch

from datetime import datetime
from typing import Dict, Any
import logging

from db import SqlDBRepository
from model import ProcessState, ETLState, AggregatedFilmwork
from state import StateStorage
from .queries import SELECT_UPDATED_MOVIES


logger = logging.getLogger(__name__)


class ETLProcessor:

    def __init__(
            self,
            sql_repository: SqlDBRepository,
            es_client: Elasticsearch,
            state_storage: StateStorage) -> None:
        self.sql_repository = sql_repository
        self.es_client = es_client
        self.state_storage = state_storage

    def run(self) -> None:
        logger.info("ETL started")
        state = self.get_current_state()
        documents_indexed = 0
        changed_movies_query = self.get_changed_movies_query(state.last_processed_time)
        for movies_chunk in self.sql_repository.execute_lazy_query(changed_movies_query):
            if not movies_chunk:
                break

            self.save_movies_chunk(movies_chunk)
            documents_indexed += len(movies_chunk)
            state.last_processed_time = AggregatedFilmwork(**movies_chunk[-1]).last_modified
            self.state_storage.save_state(state)

        logger.info("Etl ended")
        self.save_end_state(state, documents_indexed)

        import time
        time.sleep(60)

    def get_changed_movies_query(self, last_processed_time: datetime) -> str:
        return SELECT_UPDATED_MOVIES.format(last_processed_time=str(last_processed_time))

    def get_current_state(self) -> ETLState:
        prev_state = self.state_storage.retrieve_state()

        if not prev_state:
            state = ETLState()
            self.state_storage.save_state(state)
            return state

        if prev_state.process_state == ProcessState.FINISHED:
            state = ETLState(last_processed_time=prev_state.last_processed_time, process_state=ProcessState.PROCESSING)
            self.state_storage.save_state(state)
            return state
        return prev_state

    def save_end_state(self, state: ETLState, documents_indexed: int) -> None:
        state.process_state = ProcessState.FINISHED
        state.documents_indexed += documents_indexed
        state.end_time = datetime.now()
        self.state_storage.save_state(state)

    def save_movies_chunk(self, raw_movies_chunk: list[Dict[str, Any]]) -> None:
        for raw_movie in raw_movies_chunk:
            aggregated_filmwork = AggregatedFilmwork(**raw_movie)
            print(aggregated_filmwork)
