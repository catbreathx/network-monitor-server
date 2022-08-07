from pydantic import BaseModel, SecretBytes, SecretStr


class BaseUser(BaseModel):
    email: str
    first_name: str
    last_name: str


class User(BaseUser):
    pass


class UserCreate(BaseUser):
    password: SecretStr
    confirm_password: SecretStr

    class Config:
        orm_mode = True


class PutUser(BaseModel):
    class Config:
        orm_mode = True


class ChangePassword(BaseModel):
    password: SecretBytes
    confirm_password: SecretBytes

    class Config:
        orm_mode = True
