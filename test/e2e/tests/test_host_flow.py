from http import HTTPStatus

from e2e import commands, utils
from e2e.utils import assert_model_response, assert_success_response_with_id
from monitor import schema
from monitor.authentication import jwt
from monitor.database import models
from monitor.settings import app_settings


class TestHostFlow:
    def test_user_flow(self, test_user: schema.User):
        response = commands.login(test_user.email, "password")
        assert response.status_code == HTTPStatus.OK

        access_token = utils.get_access_token(response)

        host_create = schema.HostCreate(name="Control", ip_address="192.168.0.10", enabled=True)
        response = commands.create_host(host_create, access_token)
        response = commands.get_one_host(response.json()["id"], access_token)
        host1 = response.json()

        host_create = schema.HostCreate(name="Raspberry", ip_address="192.168.0.1", enabled=True)
        response = commands.create_host(host_create, access_token)
        assert_success_response_with_id(response, HTTPStatus.CREATED, 2)

        response = commands.get_one_host(response.json()["id"], access_token)
        assert response.status_code == HTTPStatus.OK
        host_response = response.json()

        assert_model_response(host_create, host_response)

        host_update = schema.HostUpdate(name="Raspberry Pi", ip_address="192.168.0.2", enabled=True)
        response = commands.update_host(host_response["id"], host_update, access_token)

        assert_success_response_with_id(response, HTTPStatus.OK, 2)

        response = commands.get_one_host(host_response["id"], access_token)
        assert response.status_code == HTTPStatus.OK
        host2 = response.json()
        assert_model_response(host_update, host2)

        response = commands.get_all_hosts(access_token)
        expected_hosts = [host1, host2]
        assert response.json() == expected_hosts

        response = commands.get_one_host(1000, access_token)
        assert response.status_code == HTTPStatus.NOT_FOUND

        expected_response = {
            "message": "Resource Not Found",
            "resource_id": "1000",
            "resource_type": "host",
        }

        assert response.json() == expected_response

    def test_when_unauthorized(self, test_user: schema.User):
        test_user = models.User(email="test@user.com")
        host_create = schema.HostCreate(name="Control", ip_address="192.168.0.10", enabled=True)
        private_key = app_settings().jwt_private_key.get_secret_value()
        jwt_token = jwt.create_jwt_token(test_user, 1, secret_key=private_key)

        response = commands.create_host(host_create, jwt_token)

        assert response.status_code == HTTPStatus.UNAUTHORIZED
