from redis import Redis

from model import ETLState
from .state_storage import StateStorage


class RedisStateStorage(StateStorage):

    def __init__(self, redis_client: Redis) -> None:
        self.redis_client = redis_client

    def save_state(self, key: str, state: ETLState) -> None:
        self.redis_client.hmset(key, state.dict())

    def retrieve_state(self, key: str) -> ETLState:
        raw_last_state = self.redis_client.hgetall(key)
        if raw_last_state:
            return ETLState(**raw_last_state)
