from typing import Optional

from ..common import DBBase, DBMetaInfo
from .constant import CONTENT_SCHEMA
from .uuid_mixin import UUIDMixin
from .timestamped_mixin import TimeStampedMixin


metainfo = DBMetaInfo(postgres_schema=CONTENT_SCHEMA, postgres_table_name='person')


class Person(DBBase, UUIDMixin, TimeStampedMixin):

    full_name: Optional[str]

    @classmethod
    def get_meta_info(cls) -> DBMetaInfo:
        return metainfo
