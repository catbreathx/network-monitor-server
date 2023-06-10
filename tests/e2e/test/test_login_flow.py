from http import HTTPStatus

from monitor import schema
from tests.e2e import api_commands, auth_commands, utils


class TestUserFlow:
    def test_user_flow(self, test_user: schema.User):
        response = auth_commands.login(test_user.email, "password")
        access_token = utils.get_access_token(response)

        payload = {
            "email": "new_user@email.com",
            "first_name": "bob",
            "last_name": "silver",
            "password": "password12!@#",
            "confirm_password": "password12!@#",
        }

        user_create = schema.UserCreate(**payload)

        response = api_commands.create_user(user_create, access_token)

        assert response.status_code == HTTPStatus.CREATED

        response_body = response.json()
        user_id = response_body["id"]

        assert isinstance(user_id, int)
