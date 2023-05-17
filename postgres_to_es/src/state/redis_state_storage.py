from redis import Redis

import json

from model import ETLState, ProcessState
from .state_storage import StateStorage


class RedisStateStorage(StateStorage):

    LAST_STATE_KEY = "etl_state"

    STATE_HISTORY = "state_history"

    def __init__(self, redis_client: Redis) -> None:
        self.redis_client = redis_client

    def save_state(self, state: ETLState) -> None:
        self.redis_client.hmset(self.LAST_STATE_KEY, state.dict())
        if state.process_state == ProcessState.FINISHED:
            self.add_history(state)

    def add_history(self, state: ETLState) -> None:
        json_state = json.dumps(state.dict())
        self.redis_client.rpush(self.STATE_HISTORY, json_state)

    def retrieve_state(self) -> ETLState:
        raw_last_state = self.redis_client.hgetall(self.LAST_STATE_KEY)

        if raw_last_state:
            last_state = ETLState(**raw_last_state)
            if last_state.process_state != ProcessState.FINISHED:
                return last_state

        new_state = ETLState()
        self.save_state(new_state)
        self.add_history(new_state)
        return new_state
