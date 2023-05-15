from pydantic import BaseModel, validator
from dateutil.parser import parse

from typing import Optional
from datetime import datetime


class TimeStampedMixin(BaseModel):

    created: Optional[datetime]

    modified: Optional[datetime]

    class Config:
        validate_assignment = True

    @validator("created", pre=True, always=True)
    def parse_created(cls, value):
        if isinstance(value, str):
            return parse(value)
        return value

    @validator("modified", pre=True, always=True)
    def parse_modified(cls, value):
        if isinstance(value, str):
            return parse(value)
        return value
