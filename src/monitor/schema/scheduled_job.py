from datetime import datetime
from typing import Any, Dict

from pydantic import BaseModel


class BaseScheduledJob(BaseModel):
    triggered_by: str
    job: str


class ScheduledJobCreate(BaseScheduledJob):
    class Config:
        orm_mode = True


class ScheduledJob(BaseScheduledJob):
    id: int
    data: Dict[str, Any]
    date_time: datetime

    class Config:
        orm_mode = True


class ScheduledJobOut(ScheduledJob):
    class Config:
        orm_mode = True
