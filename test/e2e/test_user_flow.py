from http import HTTPStatus

import requests

from monitor import schema


class TestUserFlow:
    def test_login_logout(self, test_user):
        credentials = schema.Credentials(email=test_user.email, password="password")

        response = requests.post("http://localhost:5002/api/v1/login", json=credentials.dict())

        assert response.status_code == HTTPStatus.OK
