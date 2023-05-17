from pydantic import BaseModel

from abc import ABC, abstractmethod
from typing import Dict

from .db_metainfo import DBMetaInfo


class DBBase(BaseModel, ABC):

    @classmethod
    def get_field_mapping(cls) -> Dict[str, str]:
        """Specify the mapping between postgres and pydantic model. By default it matches one to one"""
        fields = cls.__fields__.keys()
        return {field: field for field in fields}

    @abstractmethod
    def get_meta_info(cls) -> DBMetaInfo:
        pass
