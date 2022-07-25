import ipaddress

from monitor.schema.base import BaseHotasModel


class BaseHost(BaseHotasModel):
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


class HostUpdate(Host):
    class Config:
        orm_mode = True
