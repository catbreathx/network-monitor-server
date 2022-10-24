import logging

from monitor.database import db
from monitor.repository import HostRepository

logger = logging.getLogger(__name__)


def ping():
    logger.info("ping job starting!")
    db_session = db.get_session()
    host = HostRepository()
    hosts = host.get_all(db_session)

    logger.info(hosts)

    logger.info("ping job runs!")
    return hosts
