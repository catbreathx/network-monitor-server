from http import HTTPStatus
from test.e2e import commands
from typing import List

import pytest
from requests import Session

from monitor import schema
from monitor.database import models


@pytest.fixture()
def test_users_and_hosts(
    db_session: Session, test_user: schema.User, test_hosts: List[models.Host]
):
    yield test_user, test_hosts


class TestHealthCheckScheduledJob:
    def test_scheduled_job_flow(self, test_users_and_hosts: (schema.User, List[models.Host])):
        (test_user, test_hosts) = test_users_and_hosts
        access_token = commands.authenticate(test_user.email)
        response = commands.run_health_check(access_token)

        assert response.status_code == HTTPStatus.CREATED
