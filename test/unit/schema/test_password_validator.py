import pytest

from monitor.schema.password_validator import PasswordValidator

VALIDATE_PASSWORD = "1234abc[*() "


class TestPasswordValidator:
    @pytest.mark.parametrize(
        "attribute, expected_count", [("digits", 4), ("letters", 3), ("symbols", 4), ("spaces", 1)]
    )
    def test_calculation_methods(self, attribute, expected_count):
        password_validator = PasswordValidator()
        password_validator.validate(VALIDATE_PASSWORD)

        assert password_validator._count[attribute] == expected_count

    @pytest.mark.parametrize("required", [4, 3])
    def test_has_digits_when_successful_validation(self, required):
        password_validator = PasswordValidator()
        password_validator.validate(VALIDATE_PASSWORD)

        result = password_validator.has_digits(required)
        assert result == password_validator

    @pytest.mark.parametrize("required, password", [(5, "1234"), (1, "")])
    def test_has_digits_when_unsuccessful_validation(self, required, password):
        password_validator = PasswordValidator()
        password_validator.validate(password)

        with pytest.raises(ValueError) as e:
            password_validator.has_digits(required)

        assert str(e.value) == f"digits: Required {required}, found {len(password)}"

    @pytest.mark.parametrize("required", [4, 3])
    def test_has_symbols_when_successful_validation(self, required):
        password_validator = PasswordValidator()
        password_validator.validate(VALIDATE_PASSWORD)

        result = password_validator.has_symbols(required)
        assert result == password_validator

    @pytest.mark.parametrize("required, password", [(5, "!@#$"), (4, "")])
    def test_has_symbols_when_unsuccessful_validation(self, required, password):
        password_validator = PasswordValidator()
        password_validator.validate(password)

        with pytest.raises(ValueError) as e:
            password_validator.has_symbols(required)

        assert str(e.value) == f"symbols: Required {required}, found {len(password)}"

    @pytest.mark.parametrize("required", [3, 2])
    def test_has_letters_when_successful_validation(self, required):
        password_validator = PasswordValidator()
        password_validator.validate(VALIDATE_PASSWORD)

        result = password_validator.has_letters(required)
        assert result == password_validator

    @pytest.mark.parametrize("required, password", [(3, "ab"), (1, "")])
    def test_has_letters_when_unsuccessful_validation(self, required, password):
        password_validator = PasswordValidator()
        password_validator.validate(password)

        with pytest.raises(ValueError) as e:
            password_validator.has_letters(required)

        assert str(e.value) == f"letters: Required {required}, found {len(password)}"

    @pytest.mark.parametrize("required", [4, 3])
    def test_has_length_when_successful_validation(self, required):
        password_validator = PasswordValidator()
        password_validator.validate("1234")

        result = password_validator.has_length(required)
        assert result == password_validator

    @pytest.mark.parametrize("required, password", [(3, "ab"), (1, "")])
    def test_has_length_when_unsuccessful_validation(self, required, password):
        password_validator = PasswordValidator()
        password_validator.validate(password)

        with pytest.raises(ValueError) as e:
            password_validator.has_length(required)

        assert str(e.value) == f"length: Required {required}, found {len(password)}"
