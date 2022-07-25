from typing import Iterator

from sqlalchemy.orm import Session

from .host import HostRepository
from monitor.database.db import get_session


def get_db_session() -> Iterator[Session]:
    db = get_session()
    try:
        yield db
    finally:
        db.close()
