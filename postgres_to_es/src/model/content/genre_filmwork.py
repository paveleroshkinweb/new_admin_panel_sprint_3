from uuid import UUID
from typing import Optional

from ..common import DBBase, DBMetaInfo
from .constant import CONTENT_SCHEMA
from .uuid_mixin import UUIDMixin
from .timestamped_mixin import TimeStampedMixin


metainfo = DBMetaInfo(postgres_schema=CONTENT_SCHEMA, postgres_table_name='genre_film_work')


class GenreFilmwork(DBBase, UUIDMixin, TimeStampedMixin):

    film_work_id: Optional[UUID]

    genre_id: Optional[UUID]

    @classmethod
    def get_meta_info(cls) -> DBMetaInfo:
        return metainfo
