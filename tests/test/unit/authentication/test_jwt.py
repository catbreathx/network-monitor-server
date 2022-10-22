import base64

import pytest
from jose.constants import ALGORITHMS

from monitor.authentication.jwt import create_jwt_token, ALGORITHM, get_user_from_jwt_token
from monitor.database import models
from monitor.database.models import User
from monitor.exceptions import AuthenticationException
from monitor.settings import app_settings

ONE_MINUTE = 1


class TestCreateJwtToken:
    @pytest.fixture()
    def user(self) -> models.User:
        user = User(id=1, email="bob@email.com")
        return user

    def test_token_will_be_created_successfully(self, user: models.User):
        jwt_token = create_jwt_token(
            user, ONE_MINUTE, app_settings().jwt_private_key.get_secret_value(), algorithm=ALGORITHM
        )

        assert jwt_token is not None

        actual_user = get_user_from_jwt_token(
            jwt_token, public_key=app_settings().jwt_public_key, algorithms=ALGORITHM
        )

        assert user.id == actual_user.id
        assert user.email == actual_user.email

    def test_exception_thrown_when_token_fails_to_decode(self, user: models.User):
        secret_key = base64.b64encode(str.encode("secret_key")).decode("utf-8")
        public_key = base64.b64encode(str.encode("public_key")).decode("utf-8")

        jwt_token = create_jwt_token(user, ONE_MINUTE, secret_key, algorithm=ALGORITHMS.HS256)

        with pytest.raises(AuthenticationException):
            get_user_from_jwt_token(jwt_token, public_key=public_key, algorithms=ALGORITHMS.HS256)

    def test_expiration_is_populated_correctly_and_will_not_decode_when_expired(
        self, user: models.User
    ):
        jwt_token = create_jwt_token(
            user, -1, app_settings().jwt_private_key.get_secret_value(), algorithm=ALGORITHM
        )

        with pytest.raises(AuthenticationException) as e:
            get_user_from_jwt_token(
                jwt_token, public_key=app_settings().jwt_public_key, algorithms=ALGORITHM
            )

        assert str(e.value) == "Signature has expired."

    def test_when_id_is_none_and_expect_unauthorized_exception(self, user: models.User):

        user.id = None

        jwt_token = create_jwt_token(
            user, 1, app_settings().jwt_private_key.get_secret_value(), algorithm=ALGORITHM
        )

        with pytest.raises(AuthenticationException) as e:
            get_user_from_jwt_token(
                jwt_token, public_key=app_settings().jwt_public_key, algorithms=ALGORITHM
            )

        assert str(e.value) == "Unauthorized"


def decode_base64_to_str(base64_secret: str) -> str:
    key = base64.b64decode(base64_secret)
    result = key.decode("ascii")
    return result
