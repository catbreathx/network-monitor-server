from pydantic import BaseModel


class BaseHostHealthCheck(BaseModel):
    is_reachable: bool
    output_text: str
    host_id: int
    scheduled_job_id: int


class HostHealthCheckIn(BaseHostHealthCheck):
    class Config:
        orm_mode = True


class HostHealthCheckOut(BaseHostHealthCheck):
    id: int

    class Config:
        orm_mode = True
