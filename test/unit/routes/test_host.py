from http import HTTPStatus
from unittest.mock import create_autospec

import pytest

from monitor import service
from monitor.app import app
from monitor.database import models
from monitor.service import create_host_service, HostService
from test.unit.routes.base_test import BaseRouteTest
from test.unit.utils import model_list_to_json


class TestHost(BaseRouteTest):
    mock_host_service = None

    @pytest.fixture
    def host_data(self):
        hosts = [
            models.Host(
                **{'id': 1, 'name': 'Raspberry Pi', 'ip_address': '192.168.0.1', 'enabled': True}),
            models.Host(**{'id': 2, 'name': 'Apple', 'ip_address': '192.168.0.2', 'enabled': True}),
        ]

        return hosts

    @pytest.fixture(autouse=True)
    def setup_test(self):
        self.mock_host_service = create_autospec(HostService)
        mock_create_host_service = create_autospec(create_host_service,
                                                   return_value=self.mock_host_service)

        app.dependency_overrides[service.create_host_service] = mock_create_host_service

        yield

    def test_get_host(self, test_client, host_data):
        self.mock_host_service.get_all.return_value = host_data

        response = test_client.get('/api/v1/host')
        assert response.status_code == HTTPStatus.OK

        expected = model_list_to_json(host_data)
        assert response.json() == expected
