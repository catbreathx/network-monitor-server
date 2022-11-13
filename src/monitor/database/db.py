import logging

from psycopg2._psycopg import AsIs
from psycopg2.extensions import register_adapter
from pydantic.networks import IPv4Address
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session, declarative_base

from monitor.settings import app_settings

Base = declarative_base()
engine = None

logger = logging.getLogger(__name__)


def initialize_database():
    logger.info("Initializing database...")
    database_url = app_settings().database_url
    global engine
    engine = create_engine(database_url, echo=True, future=True, pool_pre_ping=True)


def test_database():
    try:
        get_session().execute("select 1")
    except OperationalError as e:
        logger.fatal(f"database not available - {e}")
        raise Exception("Database is not available")


def get_session() -> Session:
    return Session(engine)


def adapt_pydantic_ip_address(ip):
    return AsIs(repr(ip.exploded))


register_adapter(IPv4Address, adapt_pydantic_ip_address)
