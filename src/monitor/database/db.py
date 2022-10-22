from psycopg2._psycopg import AsIs
from psycopg2.extensions import register_adapter
from pydantic.networks import IPv4Address
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, Session

from monitor.settings import app_settings

Base = declarative_base()
engine = None


def initialize_database():
    postgres_url = app_settings().database_url
    global engine
    engine = create_engine(postgres_url, echo=True, future=True)


def get_session() -> Session:
    return Session(engine)


def adapt_pydantic_ip_address(ip):
    return AsIs(repr(ip.exploded))


register_adapter(IPv4Address, adapt_pydantic_ip_address)
