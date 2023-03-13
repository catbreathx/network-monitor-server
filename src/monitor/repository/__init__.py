from typing import Iterator

from sqlalchemy.orm import Session

from monitor.database.db import get_session

from .host import HostRepository
from .host_health_check import HostHealthCheckRepository
from .scheduled_job import ScheduledJobRepository
from .user import UserRepository


def get_db_session() -> Session:
    db = get_session()
    try:
        yield db
    finally:
        db.close()
