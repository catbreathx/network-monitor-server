import pytest

from monitor.authentication.jwt import create_jwt_token, decode_jwt_token
from monitor.database.models import User
from monitor.exceptions.exceptions import AuthenticationException

SECRET_KEY = " 09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"


class TestCreateJwtToken:
    @pytest.fixture()
    def user(self):
        user = User(id=1, email="bob@email.com")
        return user

    def test_token_will_be_created_successfully(self, user):
        jwt_token = create_jwt_token(user, 1, SECRET_KEY)

        assert jwt_token is not None

        actual_user = decode_jwt_token(jwt_token, secret_key=SECRET_KEY)

        assert user.id == actual_user.id
        assert user.email == actual_user.email

    def test_exception_thrown_when_token_fails_to_decode(self, user):
        jwt_token = create_jwt_token(user, 1, SECRET_KEY)

        with pytest.raises(AuthenticationException):
            decode_jwt_token(jwt_token, secret_key="abc")

    def test_expiration_is_populated_correctly_and_will_not_decode_when_expired(self, user):
        jwt_token = create_jwt_token(user, -1, SECRET_KEY)

        with pytest.raises(AuthenticationException) as e:
            decode_jwt_token(jwt_token, secret_key=SECRET_KEY)

        assert str(e.value) == "Signature has expired."
