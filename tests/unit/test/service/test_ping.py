from unittest import mock

import pytest

from monitor import schema
from monitor.database import models
from monitor.service.ping import PingService


class TestPing:
    @pytest.fixture()
    def host(self) -> models.Host:
        return models.Host(name="pi", ip_address="192.168.0.1", id=1, enabled=True)

    @mock.patch("monitor.operations.perform_ping", autospec=True)
    @mock.patch("sqlalchemy.orm.session.Session", autospec=True)
    @mock.patch("monitor.repository.scheduled_job.ScheduledJobRepository", autospec=True)
    @mock.patch("monitor.repository.host.HostRepository", autospec=True)
    @mock.patch("monitor.repository.host_health_check.HostHealthCheckRepository", autospec=True)
    def test_scheduled_job_when_successful(
        self,
        mock_host_health_check_repository: mock.Mock,
        mock_host_repository: mock.Mock,
        mock_scheduled_job_repository: mock.Mock,
        mock_db_session,
        mock_perform_ping,
        host: models.Host,
    ):
        mock_host_repository.get_all.return_value = [host]
        perform_ping_return_value = (True, "ping!")
        mock_perform_ping.return_value = perform_ping_return_value

        scheduled_job = models.ScheduledJob(id=1)
        mock_scheduled_job_repository.create_resource.return_value = scheduled_job

        ping = PingService(
            mock_db_session,
            mock_host_repository,
            mock_scheduled_job_repository,
            mock_host_health_check_repository,
        )

        ping.run_scheduled_job()

        mock_host_repository.get_all.assert_called_once()
        mock_scheduled_job_repository.create_resource.assert_called_once_with(
            mock_db_session, mock.ANY
        )

        assert isinstance(
            mock_scheduled_job_repository.create_resource.call_args.args[1],
            schema.ScheduledJobCreate,
        )

        mock_host_health_check_repository.create_resource.assert_called_once_with(
            mock_db_session, mock.ANY
        )

        actual_health_check_parameter: models.HostHealthCheck = (
            mock_host_health_check_repository.create_resource.call_args.args[1]
        )

        assert actual_health_check_parameter.output_text == perform_ping_return_value[1]
        assert actual_health_check_parameter.host_id == host.id
        assert actual_health_check_parameter.scheduled_job_id == scheduled_job.id
        assert actual_health_check_parameter.is_reachable is True

        mock_db_session.commit.assert_called_once()
