import datetime
from typing import Iterator
from unittest import mock
from unittest.mock import Mock

import sqlalchemy
from sqlalchemy.orm.collections import InstrumentedList

from monitor import repository
from monitor.database import models
from monitor.operations.email.email_notification import EmailNotification
from monitor.operations.email.health_check_report_email import (
    HealthCheckReportGenerator,
)


class TestHealthCheckReportGenerator:
    @mock.patch("monitor.operations.email.email_notification.EmailNotification", autospec=True)
    @mock.patch("monitor.repository.host.HostRepository", autospec=True)
    def test_generate_email_successfully(
        self,
        mock_host_repository: repository.HostRepository | Mock,
        mock_email_notification: EmailNotification | Mock,
        mock_db_session: sqlalchemy.orm.session.Session | Mock,
        all_hosts: Iterator[models.Host] | Mock,
    ):
        now = datetime.datetime.now()
        host_health_check = models.HostHealthCheck(
            id=1, is_reachable=False, output_text="ping failed"
        )

        mock_host_repository.get_all = mock.Mock(return_value=all_hosts)

        hosts = InstrumentedList()
        hosts.append(host_health_check)

        scheduled_job = models.ScheduledJob(date_time=now, host_health_checks=hosts)

        generator = HealthCheckReportGenerator(
            db_session=mock_db_session,
            email_sender=mock_email_notification,
            host_repository=mock_host_repository,
        )
        generator.generate_report(scheduled_job)

        mock_email_notification.send_email.assert_called_once()
        mock_host_repository.get_all.assert_called_once_with(mock_db_session)
