from datetime import datetime
from typing import Dict, Any
import logging
import time

from es import ESHandler
from db import SqlDBRepository
from model import ProcessState, ETLState, AggregatedFilmwork, ESFilmwork
from state import StateStorage
from .queries import SELECT_UPDATED_MOVIES
from .map_entities import map_dbfilmwork_to_es


logger = logging.getLogger(__name__)


class ETLProcessor:

    MOVIES_STATE_KEY = "movies_state"

    def __init__(
            self,
            sql_repository: SqlDBRepository,
            es_handler: ESHandler,
            state_storage: StateStorage,
            sleep_time: int = 0) -> None:
        self.sql_repository = sql_repository
        self.es_handler = es_handler
        self.state_storage = state_storage
        self.sleep_time = sleep_time

    def run(self) -> None:
        logger.info("ETL started")
        self.es_handler.create_index_if_not_exist(ESFilmwork.get_meta_info())

        state = self.get_current_state()
        documents_indexed = 0

        changed_movies_query = self.get_changed_movies_query(state.last_processed_time)
        for movies_chunk in self.sql_repository.execute_lazy_query(changed_movies_query):
            if not movies_chunk:
                logger.info("No new entries to process")
                break

            logger.info(f"Processing {len(movies_chunk)} movies")
            self.save_movies_chunk(movies_chunk)
            documents_indexed += len(movies_chunk)
            state.last_processed_time = AggregatedFilmwork(**movies_chunk[-1]).last_modified
            self.state_storage.save_state(self.MOVIES_STATE_KEY, state)

        logger.info("Etl ended")
        self.save_end_state(state, documents_indexed)
        time.sleep(self.sleep_time)

    def get_changed_movies_query(self, last_processed_time: datetime) -> str:
        return SELECT_UPDATED_MOVIES.format(last_processed_time=str(last_processed_time))

    def get_current_state(self) -> ETLState:
        prev_state = self.state_storage.retrieve_state(self.MOVIES_STATE_KEY)

        if not prev_state:
            state = ETLState()
            self.state_storage.save_state(self.MOVIES_STATE_KEY, state)
            return state

        if prev_state.process_state == ProcessState.FINISHED:
            state = ETLState(last_processed_time=prev_state.last_processed_time, process_state=ProcessState.PROCESSING)
            self.state_storage.save_state(self.MOVIES_STATE_KEY, state)
            return state

        return prev_state

    def save_end_state(self, state: ETLState, documents_indexed: int) -> None:
        state.process_state = ProcessState.FINISHED
        state.documents_indexed += documents_indexed
        state.end_time = datetime.now()
        self.state_storage.save_state(self.MOVIES_STATE_KEY, state)

    def save_movies_chunk(self, raw_movies_chunk: list[Dict[str, Any]]) -> None:
        es_movies_chunk = [
            map_dbfilmwork_to_es(AggregatedFilmwork(**raw_movie))
            for raw_movie in raw_movies_chunk
        ]
        self.es_handler.bulk(es_movies_chunk)
