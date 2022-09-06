from pydantic import BaseModel


class Credentials(BaseModel):
    email: str
    password: str

    class Config:
        orm_mode = True
