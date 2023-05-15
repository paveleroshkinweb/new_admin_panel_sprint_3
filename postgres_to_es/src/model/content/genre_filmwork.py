from uuid import UUID
from typing import Optional

from .uuid_mixin import UUIDMixin
from .timestamped_mixin import TimeStampedMixin


class GenreFilmwork(UUIDMixin, TimeStampedMixin):

    film_work_id: Optional[UUID]

    genre_id: Optional[UUID]
