from typing import Optional

from .uuid_mixin import UUIDMixin
from .timestamped_mixin import TimeStampedMixin


class Person(UUIDMixin, TimeStampedMixin):

    full_name: Optional[str]
