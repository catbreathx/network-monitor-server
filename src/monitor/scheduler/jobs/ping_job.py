import logging

from monitor import repository, service
from monitor.database import db

logger = logging.getLogger(__name__)


class HostPingJob:
    def run(self, *args, **kwargs):
        ping_service = service.PingService(
            db=db.get_session(),
            host_repository=repository.HostRepository(),
            scheduled_job_repository=repository.ScheduledJobRepository(),
            host_health_check_repository=repository.HostHealthCheckRepository(),
        )

        ping_service.run_scheduled_job()
