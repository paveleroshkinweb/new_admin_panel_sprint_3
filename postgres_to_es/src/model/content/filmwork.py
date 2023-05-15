from pydantic import validator

from datetime import datetime
from typing import Optional

from ..common import DBBase, DBMetaInfo
from .constant import CONTENT_SCHEMA
from .uuid_mixin import UUIDMixin
from .timestamped_mixin import TimeStampedMixin


metainfo = DBMetaInfo(postgres_schema=CONTENT_SCHEMA, postgres_table_name='film_work')


class Filmwork(DBBase, UUIDMixin, TimeStampedMixin):

    title: Optional[str]

    description: Optional[str]

    creation_date: Optional[datetime]

    file_path: Optional[str]

    type: Optional[str]

    rating: Optional[float]

    class Config:
        validate_assignment = True

    @validator('rating', pre=True, always=True)
    def parse_rating(cls, value) -> float:
        return value or 0.0

    @validator('description', pre=True, always=True)
    def parse_description(cls, value) -> str:
        return value or ''

    @validator('file_path', pre=True, always=True)
    def parse_file_path(cls, value) -> str:
        return value or ''

    @classmethod
    def get_meta_info(cls) -> DBMetaInfo:
        return metainfo
