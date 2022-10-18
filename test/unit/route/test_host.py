import json
from http import HTTPStatus
from typing import List
from unittest.mock import create_autospec

import pytest
from starlette.testclient import TestClient
from starlette_context import context

from monitor import service, schema
from monitor.app import app
from monitor.database import models
from monitor.route import authorization
from monitor.service import create_host_service, HostService
from test.unit.route.base_test import BaseRouteTest
from utils import model_list_to_json

HOST_BASE_PATH = "/api/v1/hosts"


class BaseTestHost(BaseRouteTest):
    mock_host_service: HostService = None

    @pytest.fixture
    def host_data(self) -> List[models.Host]:
        hosts = [
            models.Host(
                **{"id": 1, "name": "Raspberry Pi", "ip_address": "192.168.0.1", "enabled": True}
            ),
            models.Host(**{"id": 2, "name": "Apple", "ip_address": "192.168.0.2", "enabled": True}),
        ]

        return hosts

    @pytest.fixture(autouse=True)
    def setup_test(self) -> None:
        self.mock_host_service = create_autospec(HostService)
        self.mock_set_current_user_in_context = create_autospec(
            authorization.set_current_user_in_context
        )

        mock_create_host_service = create_autospec(
            create_host_service, spec_set=True, return_value=self.mock_host_service
        )

        user = models.User(id=1, email="user@mail.com")
        self.mock_set_current_user_in_context.return_value = user

        def set_current_user_in_context():
            context.data["user"] = self.mock_set_current_user_in_context()

        app.dependency_overrides[service.create_host_service] = mock_create_host_service
        app.dependency_overrides[
            authorization.set_current_user_in_context
        ] = set_current_user_in_context

        yield


class TestGetAllHost(BaseTestHost):
    def test_success_and_return_200(self, test_client: TestClient, host_data: List[models.Host]):
        self.mock_host_service.get_all.return_value = host_data

        response = test_client.get(HOST_BASE_PATH)
        assert response.status_code == HTTPStatus.OK

        expected = model_list_to_json(host_data)

        assert response.json() == expected
        self.mock_host_service.get_all.assert_called_once_with()

    def test_raise_exception_and_then_expect_500_exception(self, test_client: TestClient):
        self.mock_host_service.get_all.side_effect = Exception("test exception")
        response = test_client.get(HOST_BASE_PATH)

        assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR

    def test_return_authorized_when_user_is_not_valid(
        self, test_client: TestClient, host_data: List[models.Host]
    ):
        self._test_return_unauthorized_when_user_is_not_valid(test_client, path=HOST_BASE_PATH)


class TestGetOneHost(BaseTestHost):
    def test_when_resource_found_and_return_200(
        self, test_client: TestClient, host_data: List[models.Host]
    ):
        self.mock_host_service.get_one.return_value = host_data[0]

        resource_id = "1"
        response = test_client.get(f"{HOST_BASE_PATH}/{resource_id}")

        assert response.status_code == HTTPStatus.OK
        assert response.json() == host_data[0].json()

        self.mock_host_service.get_one.assert_called_once_with(resource_id)

    def test_when_resource_not_found_and_return_404(
        self, test_client: TestClient, host_data: List[models.Host]
    ):
        self.mock_host_service.get_one.return_value = None

        resource_id = "1"
        response = test_client.get(f"{HOST_BASE_PATH}/{resource_id}")

        expected_response = {
            "message": "Resource Not Found",
            "resource_id": resource_id,
            "resource_type": "host",
        }

        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json() == expected_response

    def test_return_unauthorized_when_user_is_not_valid(
        self, test_client: TestClient, host_data: List[models.Host]
    ):
        self._test_return_unauthorized_when_user_is_not_valid(
            test_client, path=f"{HOST_BASE_PATH}/1"
        )


class TestUpdateHost(BaseTestHost):
    def test_when_resource_exists_and_return_200(self, test_client: TestClient):
        resource_id = 1

        host_update = schema.HostUpdate(
            **{"name": "Pi", "ip_address": "192.168.0.2", "enabled": True}
        )
        host_data = host_update.dict()
        host_data["id"] = resource_id

        host = models.Host(**host_data)

        self.mock_host_service.update_host.return_value = host
        response = test_client.put(
            f"{HOST_BASE_PATH}/{resource_id}", json=json.loads(host_update.json())
        )

        assert response.status_code == HTTPStatus.OK
        assert response.json() == {"id": resource_id}

        self.mock_host_service.update_host.assert_called_once_with(resource_id, host_update)
