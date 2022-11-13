from datetime import datetime

from pydantic import BaseModel


class BaseScheduledJob(BaseModel):
    triggered_by: str
    job: str


class ScheduledJobCreate(BaseScheduledJob):
    class Config:
        orm_mode = True


class ScheduledJob(BaseScheduledJob):
    id: int
    ping_success: bool
    date_time: datetime

    class Config:
        orm_mode = True


class ScheduledJobOut(ScheduledJob):
    class Config:
        orm_mode = True
