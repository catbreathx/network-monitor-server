from http import HTTPStatus

from e2e import commands, utils
from monitor import schema


class TestUserFlow:
    def test_login_logout(self, test_user: schema.User):
        response = commands.login(test_user.email, "password")
        access_token = utils.get_access_token(response)

        assert response.status_code == HTTPStatus.OK

        host = schema.HostCreate(name="Raspberry", ip_address="192.168.0.1", enabled=True)
        response = commands.create_host(host, access_token)

        assert response.status_code == HTTPStatus.CREATED
        assert response.json() == {"id": 1}
