from http import HTTPStatus
from unittest import mock
from unittest.mock import create_autospec

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from monitor import exceptions, request_context
from monitor.app import app_instance
from monitor.database import models
from monitor.repository import get_db_session
from monitor.route import authorization


class BaseRouteTest:
    user = models.User(id=1, email="user@mail.com", first_name="First", last_name="Last")

    @pytest.fixture(autouse=True)
    def common_setup_test(self) -> None:
        mock_session = create_autospec(Session)
        mock_create_host_service = create_autospec(get_db_session, return_value=mock_session)

        def set_current_user_in_context():
            self.mock_set_current_user_in_context(self.user)

        self.mock_set_current_user_in_context = mock.Mock(
            autospec=True, wraps=request_context.set_user_in_context
        )

        app_instance.dependency_overrides[
            authorization.set_current_user_in_context
        ] = set_current_user_in_context

        app_instance.dependency_overrides[get_db_session] = mock_create_host_service

    @pytest.fixture(autouse=True)
    def test_client(self) -> TestClient:
        client = TestClient(app_instance)
        return client

    def _test_return_unauthorized_when_user_is_not_valid(
        self, test_client: TestClient, method: str = "GET", path: str = None
    ):
        self.mock_set_current_user_in_context.side_effect = exceptions.AuthenticationException(
            "tests"
        )
        response = test_client.request(method, path)
        assert response.status_code == HTTPStatus.UNAUTHORIZED
