from http import HTTPStatus

import requests

from monitor.schema import UserCreate


class TestUserFlow:
    def test_user_flow(self):
        payload = {
            "email": "test1@email.com",
            "first_name": "test",
            "last_name": "last",
            "password": "Pa$$w0rd1234",
            "confirm_password": "Pa$$w0rd1234",
        }

        user_create_payload = UserCreate(**payload)

        response = requests.post("http://localhost:5002/api/v1/user", json=user_create_payload)
        assert response.status_code == HTTPStatus.CREATED
