from abc import ABC, abstractmethod

from model import ETLState


class StateStorage(ABC):

    @abstractmethod
    def save_state(self, key: str, state: ETLState) -> None:
        pass

    @abstractmethod
    def retrieve_state(self, key: str) -> ETLState:
        pass
