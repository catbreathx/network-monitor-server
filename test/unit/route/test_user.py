from http import HTTPStatus
from typing import Dict, Generator
from unittest.mock import create_autospec

import pytest
from starlette.testclient import TestClient
from starlette_context import context

from monitor import service, schema
from monitor.app import app
from monitor.database import models
from monitor.route import authorization
from monitor.schema import UserCreate
from monitor.service import UserService, create_user_service
from test.unit.route.base_test import BaseRouteTest

USER_BASE_PATH = "/api/v1/users"


class BaseTestUser(BaseRouteTest):
    mock_user_service: service.UserService = None
    mock_set_current_user_in_context = None

    @pytest.fixture(autouse=True)
    def setup_test(self) -> Generator[None, None, None]:
        self.mock_user_service = create_autospec(UserService)

        mock_create_user_service = create_autospec(
            create_user_service, return_value=self.mock_user_service
        )
        self.mock_set_current_user_in_context = create_autospec(
            authorization.set_current_user_in_context
        )

        user = models.User(id=1, email="user@mail.com")
        self.mock_set_current_user_in_context.return_value = user

        def set_current_user_in_context():
            context.data["user"] = self.mock_set_current_user_in_context()

        app.dependency_overrides[
            authorization.set_current_user_in_context
        ] = set_current_user_in_context

        app.dependency_overrides[service.create_user_service] = mock_create_user_service

        yield

    @pytest.fixture()
    def post_payload(self) -> dict[str, str]:
        user = {
            "email": "user@email.com",
            "first_name": "bob",
            "last_name": "silver",
            "password": "password12!@#",
            "confirm_password": "password12!@#",
        }

        return user

    @pytest.fixture()
    def existing_user(self) -> Dict:
        user = {
            "id": 1,
            "email": "user@email.com",
            "first_name": "bob",
            "last_name": "silver",
        }

        return user


class TestPostUser(BaseTestUser):
    def test_success_and_return_201(self, test_client: TestClient, post_payload: Dict):
        user_create = UserCreate(**post_payload)
        new_user = models.User(**{"id": 1})
        self.mock_user_service.create_user.return_value = new_user

        response = test_client.post(USER_BASE_PATH, json=user_create.dict())
        assert response.status_code == HTTPStatus.CREATED

        self.mock_user_service.create_user.assert_called_once_with(user_create)

    def test_when_user_fails_validation(self, test_client: TestClient, post_payload: Dict):
        user_create = UserCreate(**post_payload)
        user_create.password = "another_password"

        response = test_client.post(USER_BASE_PATH, json=user_create.dict())
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json()["detail"][1]["msg"] == "Passwords do not match"

    def test_when_exception_thrown_and_expect_500_exception(
        self, test_client: TestClient, post_payload: Dict
    ):
        self.mock_user_service.create_user.side_effect = Exception("test exception")
        response = test_client.post(USER_BASE_PATH, json=post_payload)

        assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR

    def test_return_unauthorized_when_user_is_not_valid(self, test_client):
        self._test_return_unauthorized_when_user_is_not_valid(
            test_client, "POST", f"{USER_BASE_PATH}"
        )


class TestGetUserByGetOne(BaseTestUser):
    def test_success_and_return_200(self, test_client: TestClient, existing_user: Dict):
        user = schema.UserGetOut(**existing_user)
        self.mock_user_service.get_user_by_id.return_value = user

        response = test_client.get(f"{USER_BASE_PATH}/{user.id}")
        assert response.status_code == HTTPStatus.OK

        self.mock_user_service.get_user_by_id.assert_called_once_with(user.id)

    def test_return_unauthorized_when_user_is_not_valid(self, test_client: TestClient):
        self._test_return_unauthorized_when_user_is_not_valid(
            test_client, "GET", f"{USER_BASE_PATH}/1"
        )
