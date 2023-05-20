from pydantic import BaseModel

from uuid import UUID, uuid4
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum


class ProcessState(str, Enum):
    NEW: str = "NEW"
    PROCESSING: str = "PROCESSING"
    FINISHED: str = "FINISHED"


class ETLState(BaseModel):

    id: UUID = uuid4()

    process_state: ProcessState = ProcessState.NEW

    last_processed_time: datetime = datetime.min

    start_time: datetime = datetime.now()

    # In case of etl failure we can process some elements twice so the number of rows can be > total number in database
    documents_indexed: int = 0

    end_time: Optional[datetime]

    class Config:
        validate_assignment = True

    def dict(self) -> Dict[str, Any]:
        data = super().dict()
        for field in ('id', 'start_time', 'last_processed_time'):
            data[field] = str(data[field])
        if data['end_time'] is not None:
            data['end_time'] = str(data['end_time'])
        data = {k: v for k, v in data.items() if v is not None}
        return data
