from pydantic import BaseModel

from uuid import UUID
from enum import Enum


class RoleType(str, Enum):
    DIRECTOR: str = 'director'
    WRITER: str = 'writer'
    ACTOR: str = 'actor'


class PersonRole(BaseModel):

    person_id: UUID

    person_role: RoleType

    person_name: str
