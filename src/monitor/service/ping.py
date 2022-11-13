import logging
from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session

from monitor import operations, schema
from monitor.database import models
from monitor.repository import HostRepository, get_db_session
from monitor.repository.host_health_check import HostHealthCheckRepository
from monitor.repository.scheduled_job import ScheduledJobRepository

logger = logging.getLogger(__name__)


class PingService:
    _scheduled_job_repository: ScheduledJobRepository
    _host_health_check_repository: HostHealthCheckRepository
    _db: Session

    def __init__(
        self,
        db: Session,
        host_repository: HostRepository,
        scheduled_job_repository: ScheduledJobRepository,
        host_health_check_repository: HostHealthCheckRepository,
    ):
        self._db = db
        self._host_repository = host_repository
        self._scheduled_job_repository = scheduled_job_repository
        self._host_health_check_repository = host_health_check_repository

    def run_scheduled_job(self, triggered_by="SYSTEM") -> models.ScheduledJob | None:
        logging.debug("Starting scheduled job...")
        scheduled_job = None
        try:
            hosts: List[models.Host] = self._host_repository.get_all(self._db)
            scheduled_job = self._run_job(hosts, triggered_by)
            logger.debug(f"Scheduled job complete, scheduled job id = {scheduled_job.id}")
        except Exception as e:
            logger.error(f"Exception during job scheduled - {e}")
        finally:
            self._db.commit()

        return scheduled_job

    # todo: split this up
    def ping_host(self, host_id: int) -> (bool, str):
        host: models.Host = self._host_repository.get_one(self._db, host_id)
        result = self._perform_ping(host)
        return result

    def _perform_ping(self, host: models.Host):
        result = operations.perform_ping(host.ip_address)
        return result

    def _run_job(self, hosts: [models.Host], triggered_by: str):
        scheduled_job_create = schema.ScheduledJobCreate(
            triggered_by=triggered_by, job="Host HealthCheck"
        )
        scheduled_job: models.ScheduledJob = self._create_scheduled_job(scheduled_job_create)
        all_hosts_pinged = True

        for host in hosts:
            success, ping_output = self._perform_ping(host)
            health_check = schema.HostHealthCheckIn(
                is_reachable=success,
                output_text=ping_output,
                host_id=host.id,
                scheduled_job_id=scheduled_job.id,
            )
            all_hosts_pinged = (all_hosts_pinged == success) is True
            self._host_health_check_repository.create_resource(self._db, health_check)

        scheduled_job.data = {"success": all_hosts_pinged}
        return scheduled_job

    def _create_scheduled_job(
        self, scheduled_job_create: schema.ScheduledJobCreate
    ) -> models.ScheduledJob:
        scheduled_job: models.ScheduledJob = self._scheduled_job_repository.create_resource(
            self._db, scheduled_job_create
        )
        return scheduled_job


def create_ping_service(db_session: Session = Depends(get_db_session)) -> PingService:
    service = PingService(
        db_session,
        host_repository=HostRepository(),
        scheduled_job_repository=ScheduledJobRepository(),
        host_health_check_repository=HostHealthCheckRepository(),
    )
    return service
