import pytest
from sqlalchemy.orm import Session

from monitor.database import db


@pytest.fixture
def db_session() -> Session:
    return db.get_session()
