import pytest
from pydantic import ValidationError

from monitor.schema import UserCreate


class TestUser:
    def test_successful_password_validation(self):
        password = "password123!@#"
        UserCreate(
            email="user@email.com",
            first_name="first",
            last_name="last",
            password=password,
            confirm_password=password,
        )

    @pytest.mark.parametrize(
        "password,confirm_password",
        [("password123!@#", "PASSword123!@#"), ("password123!@#", "Apassword123!@#")],
        ids=[
            "case sensitive",
            "passwords differ",
        ],
    )
    def test_when_password_mismatch_and_raise_exception(self, password, confirm_password):
        with pytest.raises(ValidationError) as e:
            UserCreate(
                email="user@email.com",
                first_name="first",
                last_name="last",
                password=password,
                confirm_password=confirm_password,
            )

        assert str(e.value.raw_errors[0].exc) == "Passwords do not match"

    def test_when_password_is_too_weak_and_raise_exception(self):
        password = "weakpassword"
        with pytest.raises(ValidationError) as e:
            UserCreate(
                email="user@email.com",
                first_name="first",
                last_name="last",
                password=password,
                confirm_password=password,
            )

        assert str(e.value.raw_errors[0].exc) == "digits: Required 2, found 0"
