import ipaddress

from pydantic import BaseModel


class BaseHost(BaseModel):
    name: str
    ip_address: ipaddress.IPv4Address
    enabled: bool = True


class Host(BaseHost):
    id: int

    class Config:
        orm_mode = True


class HostCreate(BaseHost):
    class Config:
        orm_mode = True


class HostUpdate(BaseHost):
    class Config:
        orm_mode = True


class HostCreateOut(BaseModel):
    id: int

    class Config:
        orm_mode = True
