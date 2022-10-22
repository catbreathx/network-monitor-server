from pydantic import BaseModel


class JwtUser(BaseModel):
    id: int
    email: str

    class Config:
        orm_mode = True
