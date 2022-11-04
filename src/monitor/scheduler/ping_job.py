import logging
from typing import List

from monitor.database import db, models
from monitor.repository import HostRepository
from monitor.service import HostService

logger = logging.getLogger(__name__)


class HostPingJob:

    _repository: HostRepository = HostRepository()

    def run(self, *args, **kwargs):
        logger.debug("Running Ping Job")
        service: HostService = self._create_service()

        all_hosts: List[models.Host] = service.get_all()
        for host in all_hosts:
            pass

    def _create_service(self) -> HostService:
        return HostService(db.get_session(), self._repository)


def ping():
    logger.info("ping job starting!")
    db_session = db.get_session()
    host = HostRepository()
    hosts = host.get_all(db_session)

    logger.info(hosts)

    logger.info("ping job runs!")
    return hosts
