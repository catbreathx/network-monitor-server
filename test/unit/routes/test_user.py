from http import HTTPStatus
from unittest.mock import create_autospec

import pytest

from monitor import service
from monitor.app import app
from monitor.schema import UserCreate
from monitor.service import UserService, create_user_service
from test.unit.routes.base_test import BaseRouteTest

POST_PATH = "/api/v1/user"


class BaseTestUser(BaseRouteTest):
    mock_user_service = None

    @pytest.fixture(autouse=True)
    def setup_test(self):
        self.mock_user_service = create_autospec(UserService)
        mock_create_user_service = create_autospec(
            create_user_service, return_value=self.mock_user_service
        )

        app.dependency_overrides[service.create_user_service] = mock_create_user_service

        yield

    @pytest.fixture()
    def post_payload(self) -> dict[str, str]:
        user = {
            "email": "user@email.com",
            "first_name": "bob",
            "last_name": "silver",
            "password": "password",
            "confirm_password": "password",
        }

        return user


class TestPostUser(BaseTestUser):
    def test_success_and_return_200(self, test_client, post_payload):
        user_create = UserCreate(**post_payload)

        response = test_client.post(POST_PATH, json=user_create.dict())
        assert response.status_code == HTTPStatus.OK

        self.mock_user_service.create_user.assert_called_once_with(user_create)

    def test_when_exception_thrown_and_expect_500_exception(self, test_client, post_payload):
        self.mock_user_service.create_user.side_effect = Exception("test exception")
        response = test_client.post(POST_PATH, json=post_payload)

        assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
