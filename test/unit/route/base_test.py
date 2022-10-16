from http import HTTPStatus
from unittest.mock import create_autospec

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from monitor.app import app
from monitor.database import models
from monitor.exceptions import exceptions
from monitor.repository import get_db_session
from monitor.route import authorization
from monitor.route.authorization import set_current_user_in_context


class BaseRouteTest:
    mock_set_current_user_in_context: authorization.set_current_user_in_context = None

    @pytest.fixture(autouse=True)
    def setup_test(self):
        mock_session = create_autospec(Session)
        mock_create_host_service = create_autospec(get_db_session, return_value=mock_session)

        user = models.User(id=1, email="user@mail.com")
        mock_get_current_user = create_autospec(set_current_user_in_context, return_value=user)

        app.dependency_overrides[get_db_session] = mock_create_host_service
        app.dependency_overrides[set_current_user_in_context] = mock_get_current_user

    @pytest.fixture(autouse=True)
    def test_client(self):
        client = TestClient(app)

        return client

    def _test_return_forbidden_when_user_is_not_valid(
        self, test_client: TestClient, method: str = "GET", path: str = None
    ):
        self.mock_set_current_user_in_context.side_effect = exceptions.AuthenticationException(
            "test"
        )
        response = test_client.request(method, path)
        assert response.status_code == HTTPStatus.FORBIDDEN
