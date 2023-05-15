from pydantic import BaseModel

from typing import Dict

from .db_metainfo import DBMetaInfo


class DBBase(BaseModel):

    @classmethod
    def get_field_mapping(cls) -> Dict[str, str]:
        """Specify the mapping between postgres and pydantic model. By default it matches one to one"""
        fields = cls.__fields__.keys()
        return {field: field for field in fields}

    @classmethod
    def get_meta_info(cls) -> DBMetaInfo:
        pass
