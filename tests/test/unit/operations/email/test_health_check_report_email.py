import base64

import pytest
from fastapi_mail import ConnectionConfig
from pydantic import EmailStr

from monitor.database import models
from monitor.operations.email import schema
from monitor.operations.email.email_notification import EmailNotification


@pytest.mark.asyncio
class TestHealthCheckReportEmail:
    async def test_email_create(self, email_configuration: ConnectionConfig):
        host_windows = models.Host(name="Windows", ip_address="10.10.0.10", enabled=False, id=10)
        host_router = models.Host(name="Router", ip_address="10.10.0.1", enabled=True, id=1)
        host_rpi = models.Host(name="Raspberry Pi", ip_address="10.10.0.2", enabled=True, id=2)

        hosts = [host_windows, host_rpi, host_router]

        recipient_email = "receipient@mail.com"
        first_name = "Receipient"
        email = schema.EmailSchema(
            recipients_email=[EmailStr(recipient_email)],
            body={"hosts": hosts, "first_name": first_name},
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
            print(actual_content)
            pass
