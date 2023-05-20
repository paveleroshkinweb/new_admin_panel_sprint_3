from pydantic import BaseModel

from uuid import UUID


class Person(BaseModel):

    id: UUID

    name: str
