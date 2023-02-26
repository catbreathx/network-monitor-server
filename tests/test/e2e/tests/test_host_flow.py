from http import HTTPStatus
from test.e2e import commands
from test.e2e.utils import assert_model_response, assert_success_response

from monitor import schema
from monitor.authentication import jwt
from monitor.database import models
from monitor.settings import app_settings


class TestHostFlow:
    def test_host_flow(self, test_user: schema.User):
        access_token = commands.authenticate(test_user.email)
        host_create = schema.HostCreate(name="Control", ip_address="192.168.0.10", enabled=True)

        response = commands.create_host(host_create, access_token)
        response = commands.get_one_host(response.json()["id"], access_token)
        host1 = response.json()

        host_create = schema.HostCreate(name="Raspberry", ip_address="192.168.0.1", enabled=True)

        response = commands.create_host(host_create, access_token)
        assert_success_response(response, HTTPStatus.CREATED)

        response = commands.get_one_host(response.json()["id"], access_token)
        assert response.status_code == HTTPStatus.OK
        host_response = response.json()

        assert_model_response(host_create, host_response)

        host_update = schema.HostUpdate(name="Raspberry Pi", ip_address="192.168.0.2", enabled=True)

        response = commands.update_host(host_response["id"], host_update, access_token)

        assert_success_response(response, HTTPStatus.OK)

        response = commands.get_one_host(host_response["id"], access_token)
        assert response.status_code == HTTPStatus.OK
        host2 = response.json()
        assert_model_response(host_update, host2)

        response = commands.get_all_hosts(access_token)
        expected_hosts = [host1, host2]
        assert response.json() == expected_hosts

        unknown_resource_id = 1000
        response = commands.get_one_host(unknown_resource_id, access_token)
        assert response.status_code == HTTPStatus.NOT_FOUND

        expected_response = {
            "message": "Resource Not Found",
            "resource_id": unknown_resource_id,
            "resource_type": "host",
        }

        assert response.json() == expected_response

    def test_when_unauthorized(self, test_user: schema.User):
        test_user = models.User(email="tests@user.com")
        host_create = schema.HostCreate(name="Control", ip_address="192.168.0.10", enabled=True)
        private_key = app_settings().jwt_private_key.get_secret_value()
        jwt_token = jwt.create_jwt_token(test_user, 1, secret_key=private_key)

        response = commands.create_host(host_create, jwt_token)

        assert response.status_code == HTTPStatus.UNAUTHORIZED
