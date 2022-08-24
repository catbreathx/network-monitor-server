import re
from typing import Dict

regex = dict(
    digits=re.compile(r"\d+"),
    letters=re.compile(r"[a-zA-Z]+"),
    symbols=re.compile(r"[`()~!@#$%^&*\(\)\-_=+\[{}\]\\|;:\'\",<.>/?€£¥₹]+"),
    spaces=re.compile(r"[\s]+"),
)


class PasswordValidator:
    _count: Dict

    def __init__(self) -> None:
        super().__init__()

    def validate(self, password):
        self._count = {"length": len(password)}

        for letter in password:
            for pattern in regex:
                if pattern not in self._count:
                    self._count[pattern] = 0

                if regex[pattern].match(letter):
                    self._count[pattern] = self._count[pattern] + 1
                    continue

    def has_digits(self, expected):
        self._check_password_attribute(expected, "digits")
        return self

    def has_symbols(self, expected):
        self._check_password_attribute(expected, "symbols")
        return self

    def has_letters(self, expected):
        self._check_password_attribute(expected, "letters")
        return self

    def has_length(self, expected):
        self._check_password_attribute(expected, "length")
        return self

    def _check_password_attribute(self, required, attribute_type):
        actual: int = self._count.get(attribute_type, 0)

        if actual < required:
            raise ValueError(f"{attribute_type}: Required {required}, found {actual}")
