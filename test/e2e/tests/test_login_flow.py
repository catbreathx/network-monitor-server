from http import HTTPStatus

from e2e import commands, utils
from monitor import schema
from monitor.schema import UserCreate


class TestUserFlow:
    def test_user_flow(self, test_user: schema.User):
        response = commands.login(test_user.email, "password")
        access_token = utils.get_access_token(response)

        payload = {
            "email": "new_user@email.com",
            "first_name": "bob",
            "last_name": "silver",
            "password": "password12!@#",
            "confirm_password": "password12!@#",
        }

        user_create = UserCreate(**payload)

        response = commands.create_user(user_create, access_token)

        assert response.status_code == HTTPStatus.CREATED

        response_body = response.json()
        user_id = response_body["id"]

        assert isinstance(user_id, int)
