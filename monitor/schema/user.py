from builtins import ValueError
from typing import Union

from pydantic import BaseModel, validator


class BaseUser(BaseModel):
    email: str
    first_name: str
    last_name: str


class User(BaseUser):
    pass


class UserCreate(BaseUser):
    password: str
    confirm_password: str

    @validator("password")
    def validate_password(cls, value: str, values: dict[str : Union[str, int, bool]]):
        return value

    @validator("confirm_password")
    def passwords_match(cls, value: str, values: dict[str : Union[str, int, bool]]):
        password = values.get("password", "")
        if value != password:
            raise ValueError("Passwords do not match")

        return value

    class Config:
        orm_mode = True


class PutUser(BaseModel):
    class Config:
        orm_mode = True


class ChangePassword(BaseModel):
    password: str
    confirm_password: str

    class Config:
        orm_mode = True
