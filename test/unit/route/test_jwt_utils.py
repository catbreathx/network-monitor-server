from monitor.route.jwt_utils import create_access_token, decode_access_token
from monitor.settings import app_settings


class TestCreateAccessToken:
    def test_encrypt_and_decrypt(self):
        email = "user@test.com"
        secret_key = app_settings().jwt_private_key
        jwt_token = create_access_token(
            email, expires_minutes=1, secret_key=secret_key.get_secret_value()
        )

        actual_token = decode_access_token(
            jwt_token, public_key=secret_key.get_secret_value(), algorithms="RS512"
        )

        assert actual_token["sub"] == email
