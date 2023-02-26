import logging

from monitor import repository, service
from monitor.database import db, models

logger = logging.getLogger(__name__)


class HostPingJob:
    def run(self, *args, **kwargs):
        ping_service = service.PingService(
            db=db.get_session(),
            host_repository=repository.HostRepository(),
            scheduled_job_repository=repository.ScheduledJobRepository(),
            host_health_check_repository=repository.HostHealthCheckRepository(),
        )

        scheduled_job = ping_service.run_scheduled_job()

        if scheduled_job and should_produce_report(scheduled_job):
            host_health_check_service = service.create_host_health_check_service()
            host_health_check_service.construct_email_report(scheduled_job)

    # host_health_check = service.HealthCheck()


def should_produce_report(scheduled_job: models.ScheduledJob):
    """
    Determines if a report should be produced by checking hosts that failed the health check.
    :param scheduled_job: models.ScheduledJob
    :return: bool - if a report should be produced
    """
    host_health_checks = scheduled_job.host_health_checks
    result = True
    for host_health_check in host_health_checks:
        if host_health_check.is_reachable is False:
            result = False
            break

    return result
