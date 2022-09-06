from http import HTTPStatus

import pytest
import requests

from monitor.schema import UserCreate


@pytest.fixture(autouse=True)
def setup_test_user(test_user):
    pass


class TestUserFlow:
    def test_user_flow(self):
        payload = {
            "email": "user@email.com",
            "first_name": "bob",
            "last_name": "silver",
            "password": "password12!@#",
            "confirm_password": "password12!@#",
        }

        user_create_payload = UserCreate(**payload)

        response = requests.post(
            "http://localhost:5002/api/v1/user", json=user_create_payload.dict()
        )

        assert response.status_code == HTTPStatus.CREATED
