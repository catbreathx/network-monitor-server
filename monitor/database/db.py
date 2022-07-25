from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, Session

from monitor.settings.settings import get_app_settings

Base = declarative_base()
engine = None


def initialize_database():
    postgres_url = get_app_settings().database_url
    global engine
    engine = create_engine(postgres_url, echo=True, future=True)


def get_session() -> Session:
    return Session(engine)
