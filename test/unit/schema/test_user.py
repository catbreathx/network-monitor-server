import pytest
from pydantic import ValidationError

from monitor.schema import UserCreate


class TestUser:
    def test_successful_password_validation(self):
        UserCreate(
            email="user@email.com",
            first_name="first",
            last_name="last",
            password="password1",
            confirm_password="password1",
        )

    @pytest.mark.parametrize(
        "password,confirm_password",
        [("password2", "Password2"), ("pass", "Password")],
        ids=[
            "case sensitive",
            "passwords differ",
        ],
    )
    def test_unsuccessful_password_validation_and_raise_exception(self, password, confirm_password):
        with pytest.raises(ValidationError) as e:
            UserCreate(
                email="user@email.com",
                first_name="first",
                last_name="last",
                password=password,
                confirm_password=confirm_password,
            )

        assert str(e.value.raw_errors[0].exc) == "Passwords do not match"
