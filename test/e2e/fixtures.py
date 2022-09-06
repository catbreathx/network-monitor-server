import pytest
from sqlalchemy.orm import Session

from monitor.database import db, models


@pytest.fixture
def db_session() -> Session:
    return db.get_session()


@pytest.fixture
def test_user(db_session: Session):
    user = models.User(
        first_name="test",
        last_name="user",
        email="test_user@email.com",
        password="password",
        enabled=True,
        account_confirmed=True,
    )

    db_session.add(user)
    db.get_session().commit()
