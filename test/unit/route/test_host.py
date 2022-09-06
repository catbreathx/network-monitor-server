from http import HTTPStatus
from unittest.mock import create_autospec

import pytest

from monitor import service
from monitor.app import app
from monitor.database import models
from monitor.service import create_host_service, HostService
from test.unit.route.base_test import BaseRouteTest
from test.unit.utils import model_list_to_json, model_to_json

GET_PATH = "/api/v1/host"


class BaseTestHost(BaseRouteTest):
    mock_host_service: HostService = None

    @pytest.fixture
    def host_data(self):
        hosts = [
            models.Host(
                **{"id": 1, "name": "Raspberry Pi", "ip_address": "192.168.0.1", "enabled": True}
            ),
            models.Host(**{"id": 2, "name": "Apple", "ip_address": "192.168.0.2", "enabled": True}),
        ]

        return hosts

    @pytest.fixture(autouse=True)
    def setup_test(self):
        self.mock_host_service = create_autospec(HostService)
        mock_create_host_service = create_autospec(
            create_host_service, return_value=self.mock_host_service
        )

        app.dependency_overrides[service.create_host_service] = mock_create_host_service

        yield


class TestGetAllHost(BaseTestHost):
    def test_success_and_return_200(self, test_client, host_data):
        self.mock_host_service.get_all.return_value = host_data

        response = test_client.get(GET_PATH)
        assert response.status_code == HTTPStatus.OK

        expected = model_list_to_json(host_data)
        assert response.json() == expected

    def test_raise_exception_and_then_expect_500_exception(self, test_client):
        self.mock_host_service.get_all.side_effect = Exception("test exception")
        response = test_client.get(GET_PATH)
        assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR


class TestGetOneHost(BaseTestHost):
    def test_when_resource_found_and_return_200(self, test_client, host_data):
        self.mock_host_service.get_one.return_value = host_data[0]

        resource_id = "1"
        response = test_client.get(f"{GET_PATH}/{resource_id}")

        expect = model_to_json(host_data[0])
        assert response.status_code == HTTPStatus.OK
        assert response.json() == expect

    def test_when_resource_not_found_and_return_404(self, test_client, host_data):
        self.mock_host_service.get_one.return_value = None
        resource_id = "1"
        response = test_client.get(f"{GET_PATH}/{resource_id}")

        expected_response = {
            "message": "Resource Not Found",
            "resource_id": resource_id,
            "resource_type": "host",
        }

        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json() == expected_response