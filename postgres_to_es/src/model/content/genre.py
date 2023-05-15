from pydantic import validator

from typing import Optional

from ..common import DBBase, DBMetaInfo
from .constant import CONTENT_SCHEMA
from .uuid_mixin import UUIDMixin
from .timestamped_mixin import TimeStampedMixin


metainfo = DBMetaInfo(postgres_schema=CONTENT_SCHEMA, postgres_table_name='genre')


class Genre(DBBase, UUIDMixin, TimeStampedMixin):

    name: Optional[str]

    description: Optional[str]

    class Config:
        validate_assignment = True

    @validator('description', pre=True, always=True)
    def parse_description(cls, value):
        return value or ''

    @classmethod
    def get_meta_info(cls) -> DBMetaInfo:
        return metainfo
