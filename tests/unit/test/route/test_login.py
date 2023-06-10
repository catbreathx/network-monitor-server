from http import HTTPStatus
from typing import Generator
from unittest import mock
from unittest.mock import create_autospec

import pytest
from starlette.testclient import TestClient

from monitor import schema, service
from monitor.app import app_instance
from monitor.database import models
from tests.unit.test.route.base_test import BaseRouteTest

POST_PATH = "/auth/v1/login"


class BaseLoginTest(BaseRouteTest):
    mock_login_service: service.LoginService

    @pytest.fixture(autouse=True)
    def setup_test(self) -> Generator[None, None, None]:
        self.mock_login_service: mock.Mock = create_autospec(service.LoginService)
        mock_create_login_service = create_autospec(
            service.create_login_service, return_value=self.mock_login_service
        )

        app_instance.dependency_overrides[service.create_login_service] = mock_create_login_service

        yield


class TestLogin(BaseLoginTest):
    def test_login_successfully_and_expect_jwt_authorization_in_header(
        self, test_client: TestClient
    ):
        user = models.User(email="someone@email.com")
        self.mock_login_service.authenticate_login.return_value = user

        credentials = schema.Credentials(email="user@tests.com", password="password")
        actual_response = test_client.post(POST_PATH, json=credentials.dict())

        assert actual_response.status_code == HTTPStatus.OK
        json = actual_response.json()

        assert json["access_token"].startswith("ey")
        assert json["refresh_token"].startswith("ey")

        self.mock_login_service.authenticate_login.assert_called_once_with(credentials)
