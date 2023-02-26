import datetime
from http import HTTPStatus
from test.unit.tests.route.base_test import BaseRouteTest
from typing import Generator
from unittest import mock
from unittest.mock import create_autospec

import pytest
from starlette.testclient import TestClient

from monitor import service
from monitor.app import app_instance
from monitor.database import models

SCHEDULED_JOB_BASE_PATH = "/api/v1/scheduledjob"
SCHEDULED_JOB_PATH = SCHEDULED_JOB_BASE_PATH + "/ping"


SCHEDULED_JOB_DATE = datetime.datetime(year=2022, month=11, day=13, hour=14, minute=0, second=0)


class BaseScheduledJob(BaseRouteTest):
    mock_ping_service: service.PingService = None

    @pytest.fixture(autouse=True)
    def setup_test(self) -> Generator[None, None, None]:
        self.mock_ping_service: service.PingService | mock.Mock = create_autospec(
            service.PingService
        )

        mock_create_ping_service = create_autospec(
            service.create_ping_service, return_value=self.mock_ping_service
        )

        app_instance.dependency_overrides[service.create_ping_service] = mock_create_ping_service

        yield


class TestPingScheduledJob(BaseScheduledJob):
    def test_success_and_return_201(self, test_client: TestClient):
        scheduled_job = models.ScheduledJob(
            id=1,
            data={"success": True},
            job="Ping Host Scheduled Job",
            triggered_by=self.user.full_name,
            date_time=SCHEDULED_JOB_DATE,
        )

        self.mock_ping_service.run_scheduled_job.return_value = scheduled_job

        response = test_client.post(SCHEDULED_JOB_PATH)
        assert response.status_code == HTTPStatus.CREATED

        self.mock_ping_service.run_scheduled_job.assert_called_once_with(
            triggered_by=self.user.full_name
        )

    def test_when_exception_thrown_and_expect_500_exception(self, test_client: TestClient):
        self.mock_ping_service.run_scheduled_job.side_effect = Exception("tests exception")
        response = test_client.post(SCHEDULED_JOB_PATH)

        assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR

    def test_return_unauthorized_when_user_is_not_valid(self, test_client):
        self._test_return_unauthorized_when_user_is_not_valid(
            test_client, "POST", f"{SCHEDULED_JOB_PATH}"
        )
