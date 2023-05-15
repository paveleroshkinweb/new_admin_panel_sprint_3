from pydantic import validator

from typing import Optional

from .uuid_mixin import UUIDMixin
from .timestamped_mixin import TimeStampedMixin


class Genre(UUIDMixin, TimeStampedMixin):

    name: Optional[str]

    description: Optional[str]

    class Config:
        validate_assignment = True

    @validator('description', pre=True, always=True)
    def parse_description(cls, value):
        return value or ''
