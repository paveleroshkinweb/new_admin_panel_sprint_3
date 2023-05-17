from abc import ABC, abstractmethod
from typing import Generator, List, Dict


class SqlDBRepository(ABC):

    @abstractmethod
    def execute_lazy_query(
        self,
        query: str,
        chunk_size: int = 1024
    ) -> Generator[List[Dict], None, None]:
        pass
