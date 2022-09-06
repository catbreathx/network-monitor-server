from typing import Union

from sqlalchemy import TypeDecorator, Text
from sqlalchemy.engine import Dialect

from monitor.database.utils import PasswordHash

HASHING_ROUND = 12


class Password(TypeDecorator):
    impl = Text

    def __init__(self, rounds: int = HASHING_ROUND, **kwargs) -> None:
        self.rounds = rounds
        super().__init__(**kwargs)

    def process_bind_param(self, value: Union[str, PasswordHash], dialect: Dialect) -> None:
        if isinstance(value, str):
            password_hash = self._hash_password(value)
        else:
            password_hash = value

        return password_hash.hash.decode("utf-8")

    def process_result_value(self, value: str, dialect: Dialect) -> PasswordHash:
        result = PasswordHash(value)
        return result

    def validator(self, password: str):
        hashed_password = self._hash_password(password)
        return hashed_password

    def _hash_password(self, value):
        result = None
        if isinstance(value, str):
            result = PasswordHash.new(value, self.rounds)

        return result
