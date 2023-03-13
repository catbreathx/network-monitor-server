import base64
from typing import Iterator

import pytest
from fastapi_mail import ConnectionConfig
from pydantic import EmailStr

from monitor.database import models
from monitor.operations.email import schema, template_data
from monitor.operations.email.email_notification import EmailNotification


@pytest.mark.asyncio
class TestHealthCheckReportEmail:
    async def test_email_create(
        self,
        scheduled_jobs: Iterator[models.ScheduledJob],
        all_hosts: [models.Host],
        email_configuration: ConnectionConfig,
    ):
        scheduled_job = yield scheduled_jobs

        recipient_email = "receipient@mail.com"
        first_name = "Receipient"
        data = template_data.HealthCheckReport(
            scheduled_job, all_hosts, scheduled_job.host_health_checks
        )

        email = schema.EmailSchema(
            recipients_email=[EmailStr(recipient_email)],
            body={"data": data.json(), "first_name": first_name},
        )

        email_notification = EmailNotification(email_configuration)
        fastmail = email_notification._fastmail
        fastmail.config.SUPPRESS_SEND = 1

        with fastmail.record_messages() as outbox:
            await email_notification.send_email(email)
            actual_email = outbox[0]
            assert actual_email["to"] == recipient_email
            actual_content_base64 = actual_email.get_payload()[0].get_payload()
            actual_content_base64 = bytes(actual_content_base64, "utf-8")
            actual_content = base64.urlsafe_b64decode(actual_content_base64).decode()
            assert get_expected_email() == actual_content


def get_expected_email() -> str:
    return """
Hi Receipient,

Here's the failure health check report for 2022-11-03 02:30:00.

<table>
    <tr>
        <th>Host</th>
        <th>Reason of Failure</th>
    </tr>

    <tr>

                <td>Windows</td>
                <td>10.10.0.10</td>
                <td>Unknown Host</td>


    </tr>
</table>

Thanks
    """.strip()
