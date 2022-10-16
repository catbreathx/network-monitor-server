from http import HTTPStatus
from unittest.mock import create_autospec

import pytest

from monitor import schema, service
from monitor.app import app
from monitor.database import models
from monitor.service import LoginService, create_login_service
from unit.route.base_test import BaseRouteTest

POST_PATH = "/api/v1/login"


class BaseLoginTest(BaseRouteTest):
    mock_login_service: LoginService

    @pytest.fixture(autouse=True)
    def setup_test(self):
        self.mock_login_service = create_autospec(LoginService)
        mock_create_login_service = create_autospec(
            create_login_service, return_value=self.mock_login_service
        )

        app.dependency_overrides[service.create_login_service] = mock_create_login_service

        yield


class TestLogin(BaseLoginTest):
    def test_login_successfully_and_expect_jwt_authorization_in_header(self, test_client):
        user = models.User(email="someone@email.com")
        self.mock_login_service.authenticate_login.return_value = user

        credentials = schema.Credentials(email="user@test.com", password="password")
        actual_response = test_client.post(POST_PATH, json=credentials.dict())

        assert actual_response.status_code == HTTPStatus.OK
        json = actual_response.json()

        assert json["access_token"].startswith("ey")
        assert json["refresh_token"].startswith("ey")
