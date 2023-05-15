from pydantic import BaseModel

from typing import Optional
from uuid import UUID


class UUIDMixin(BaseModel):

    id: Optional[UUID]
