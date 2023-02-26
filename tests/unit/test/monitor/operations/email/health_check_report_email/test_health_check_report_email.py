import datetime
from unittest import mock
from unittest.mock import Mock

from sqlalchemy.orm.collections import InstrumentedList

from monitor.database import models
from monitor.operations.email.email_notification import EmailNotification
from monitor.operations.email.health_check_report_email import (
    HealthCheckReportGenerator,
)


class TestHealthCheckReportGenerator:
    @mock.patch("monitor.operations.email.email_notification.EmailNotification", autospec=True)
    def test_generate_email_successfully(self, mock_email_notification: EmailNotification | Mock):
        now = datetime.datetime.now()
        host_health_check = models.HostHealthCheck(
            id=1, is_reachable=False, output_text="ping failed"
        )

        hosts = InstrumentedList()
        hosts.append(host_health_check)

        scheduled_job = models.ScheduledJob(date_time=now, host_health_checks=hosts)

        generator = HealthCheckReportGenerator(None, email_sender=mock_email_notification)
        generator.generate_report(scheduled_job)

        mock_email_notification.send_email.assert_called_once()
