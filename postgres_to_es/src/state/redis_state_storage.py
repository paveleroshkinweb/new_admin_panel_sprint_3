from redis import Redis

from model import ETLState
from .state_storage import StateStorage


class RedisStateStorage(StateStorage):

    STATE_KEY = "state"

    def __init__(self, redis_client: Redis) -> None:
        self.redis_client = redis_client

    def save_state(self, state: ETLState) -> None:
        self.redis_client.hmset(self.STATE_KEY, state.dict())

    def retrieve_state(self) -> ETLState:
        raw_last_state = self.redis_client.hgetall(self.STATE_KEY)
        if raw_last_state:
            return ETLState(**raw_last_state)
