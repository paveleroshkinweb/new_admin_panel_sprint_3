from pydantic import BaseModel

from typing import Dict

from .db_metainfo import DBMetaInfo


class DBBase(BaseModel):

    @classmethod
    def get_field_mapping(cls) -> Dict[str, str]:
        """Specify the mapping between sqlite and postgres fields"""
        return cls.FIELD_MAPPING

    @classmethod
    def get_meta_info(cls) -> DBMetaInfo:
        return cls.META_INFO
