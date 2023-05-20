from pydantic import BaseModel, Extra

from uuid import UUID
from datetime import datetime

from .person_role import PersonRole


class AggregatedFilmwork(BaseModel, extra=Extra.allow):

    id: UUID

    title: str

    description: str | None

    rating: float

    persons: list[PersonRole]

    genres: list[str]

    last_modified: datetime
