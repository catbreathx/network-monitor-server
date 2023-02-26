from fastapi import Depends
from sqlalchemy.orm import Session

from monitor.database import models
from monitor.operations import email
from monitor.repository import HostHealthCheckRepository, get_db_session
from monitor.settings import app_settings


class HostHealthCheckService:
    _host_health_check_repository: HostHealthCheckRepository
    _health_check_report_generator = email.HealthCheckReportGenerator

    def __init__(self, db: Session, host_health_check: HostHealthCheckRepository):
        self._host_health_check_repository = host_health_check
        self._health_check_report_generator = email.create_report_generator(
            db_session=db, app_settings=app_settings()
        )

    def construct_email_report(self, scheduled_job: models.ScheduledJob):
        self._health_check_report_generator.generate_report(scheduled_job)


def create_host_health_check_service(
    db_session: Session = Depends(get_db_session),
) -> HostHealthCheckService:
    service = HostHealthCheckService(db_session, HostHealthCheckRepository())
    return service
