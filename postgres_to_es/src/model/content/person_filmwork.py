from uuid import UUID
from typing import Optional

from .uuid_mixin import UUIDMixin
from .timestamped_mixin import TimeStampedMixin


class PersonFilmwork(UUIDMixin, TimeStampedMixin):

    film_work_id: Optional[UUID]

    person_id: Optional[UUID]

    role: Optional[str]
