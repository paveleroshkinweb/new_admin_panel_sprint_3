from pydantic import BaseModel

from abc import ABC, abstractclassmethod, abstractmethod
from typing import Any


class ESMeta(BaseModel):

    index: str

    version: str


class ESModel(BaseModel, ABC):

    @abstractclassmethod
    def get_meta_info(cls) -> ESMeta:
        pass

    @abstractmethod
    def get_document_id(self) -> Any:
        pass
