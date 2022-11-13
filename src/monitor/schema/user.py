import typing
from builtins import ValueError

from pydantic import BaseModel, root_validator, validator

from monitor.schema.password_validator import PasswordValidator


class BaseUser(BaseModel):
    email: str
    first_name: str
    last_name: str | None

    @root_validator
    def normalize_values(cls, values: typing.Dict) -> typing.Dict:
        values["email"]: str = values["email"].lower()
        return values


class User(BaseUser):
    pass


class UserCreate(BaseUser):
    password: str
    confirm_password: str

    @validator("password")
    def validate_password(cls, value: str, values: dict[str:[str, int, bool]]):
        validator = PasswordValidator()
        validator.validate(value)

        try:
            validator.has_digits(2).has_length(10).has_letters(8).has_symbols(2)
        except ValueError as e:
            raise ValueError(e)

        return value

    @validator("confirm_password")
    def passwords_match(cls, value: str, values: dict[str, [str, int, bool]]):
        password = values.get("password", "")
        if value != password:
            raise ValueError("Passwords do not match")

        return value

    class Config:
        orm_mode = True
        exclude = {"confirm_password"}


class UserUpdate(BaseModel):
    class Config:
        orm_mode = True


class ChangePassword(BaseModel):
    password: str
    confirm_password: str

    class Config:
        orm_mode = True


class UserCreateOut(BaseModel):
    id: int

    class Config:
        orm_mode = True


class UserGetOut(User):
    id: int

    class Config:
        orm_mode = True
