from unittest.mock import create_autospec

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from monitor.app import app
from monitor.repository import get_db_session


class BaseRouteTest:

    @pytest.fixture(autouse=True)
    def setup_test(self):
        mock_session = create_autospec(Session)
        mock_create_host_service = create_autospec(get_db_session,
                                                   return_value=mock_session)

        app.dependency_overrides[get_db_session] = mock_create_host_service

    @pytest.fixture(autouse=True)
    def test_client(self):
        client = TestClient(app)

        return client
