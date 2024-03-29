import asyncio
import os
from pathlib import Path

from fastapi_mail import ConnectionConfig
from pydantic import EmailStr
from requests import Session

from monitor import repository
from monitor.database import models
from monitor.operations.email import schema, template_data
from monitor.operations.email.email_notification import EmailNotification
from monitor.settings.app_settings import Settings


class HealthCheckReportGenerator:
    _db_session: Session
    _host_repository: repository.HostRepository
    _email_sender: EmailNotification

    def __init__(
        self,
        db_session: Session,
        email_sender: EmailNotification,
        host_repository: repository.HostRepository,
    ) -> None:
        super().__init__()
        self._db_session = db_session
        self._email_sender = email_sender
        self._host_repository = host_repository

    def generate_report(self, scheduled_job: models.ScheduledJob) -> None:
        hosts = self._host_repository.get_all(self._db_session)
        data = template_data.HealthCheckReport(
            scheduled_job=scheduled_job,
            hosts=hosts,
            host_health_checks=scheduled_job.host_health_checks,
        )

        recipients = [EmailStr("stewart01@mac.com")]
        body = {"data": data.json(), "first_name": "test@email.com"}
        email = schema.EmailSchema(recipients_email=recipients, body=body)
        asyncio.run(self._email_sender.send_email(email))


def create_report_generator(
    db_session: Session, app_settings: Settings
) -> HealthCheckReportGenerator:
    template_folder = os.path.join(os.getcwd(), app_settings.email_template_directory)

    connection_config = ConnectionConfig(
        MAIL_USERNAME=app_settings.email_username,
        MAIL_PASSWORD=app_settings.email_password,
        MAIL_PORT=app_settings.email_port,
        MAIL_SERVER=app_settings.email_server,
        TEMPLATE_FOLDER=Path(template_folder),
        MAIL_STARTTLS=app_settings.email_starttls,
        MAIL_SSL_TLS=app_settings.email_ssl_tls,
        MAIL_FROM=EmailStr(app_settings.mail_from),
    )
    email_notification = EmailNotification(connection_config)
    result = HealthCheckReportGenerator(
        db_session=db_session,
        email_sender=email_notification,
        host_repository=repository.HostRepository(),
    )

    return result
