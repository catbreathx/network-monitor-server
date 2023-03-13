import datetime
import os
from pathlib import Path
from typing import Iterator
from unittest import mock

import pytest
import sqlalchemy
from fastapi_mail import ConnectionConfig
from pydantic import EmailStr
from sqlalchemy.orm.collections import InstrumentedList

from monitor.database import models


@pytest.fixture
@mock.patch("sqlalchemy.orm.session.Session", autospec=True)
def mock_db_session(
    mock_db_session: sqlalchemy.orm.session.Session,
) -> sqlalchemy.orm.session.Session:
    return mock_db_session


@pytest.fixture
def datetime_now() -> datetime.datetime:
    now = datetime.datetime(year=2022, month=11, day=3, hour=2, minute=30, second=0)
    yield now


@pytest.fixture
def good_hosts() -> Iterator[models.Host]:
    host_router = models.Host(name="Router", ip_address="10.10.0.1", enabled=True, id=1)
    host_rpi = models.Host(name="Raspberry Pi", ip_address="10.10.0.2", enabled=True, id=2)

    yield [host_router, host_rpi]


@pytest.fixture
def bad_hosts() -> Iterator[models.Host]:
    host_windows = models.Host(name="Windows", ip_address="10.10.0.10", enabled=False, id=10)
    yield [host_windows]


@pytest.fixture
def all_hosts(
    good_hosts: Iterator[models.Host], bad_hosts: Iterator[models.Host]
) -> Iterator[models.Host]:
    hosts = good_hosts + bad_hosts
    yield hosts


@pytest.fixture
def host_health_check_success(good_hosts: list[models.Host]) -> Iterator[models.HostHealthCheck]:
    host = good_hosts[0]
    model = models.HostHealthCheck(id=1, is_reachable=True, output_text="ping 2m", host_id=host.id)

    yield [model]


@pytest.fixture
def host_health_check_failure(bad_hosts: list[models.Host]) -> Iterator[models.HostHealthCheck]:
    host = bad_hosts[0]
    model = models.HostHealthCheck(
        id=10, is_reachable=False, output_text="Unknown Host", host_id=host.id
    )

    yield [model]


@pytest.fixture
def scheduled_jobs(
    datetime_now: datetime.datetime,
    host_health_check_success: list[models.HostHealthCheck],
    host_health_check_failure: list[models.HostHealthCheck],
) -> Iterator[models.ScheduledJob]:
    host_health_checks: InstrumentedList[models.HostHealthCheck] = InstrumentedList()
    [
        host_health_checks.append(host)
        for host in host_health_check_success + host_health_check_failure
    ]

    scheduled_job = models.ScheduledJob(
        id=1,
        data={"result": "some hosts failed"},
        triggered_by="system",
        date_time=datetime_now,
        host_health_checks=host_health_checks,
    )

    for host_health_check in host_health_checks:
        host_health_check.scheduled_job = scheduled_job
        host_health_check.scheduled_job_id = scheduled_job.id

    yield scheduled_job


@pytest.fixture
def email_configuration():
    template_folder = os.path.join(os.getcwd(), "resources/templates/email")
    result = ConnectionConfig(
        MAIL_USERNAME="username",
        MAIL_PASSWORD="password",
        MAIL_FROM=EmailStr("sender@mail.com"),
        MAIL_PORT=465,
        MAIL_SERVER="mail server",
        MAIL_STARTTLS=False,
        MAIL_SSL_TLS=True,
        USE_CREDENTIALS=True,
        VALIDATE_CERTS=True,
        SUPPRESS_SEND=1,
        TEMPLATE_FOLDER=Path(template_folder),
    )

    return result
