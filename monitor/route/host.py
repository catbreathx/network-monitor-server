from http import HTTPStatus

from fastapi import Depends, APIRouter

from monitor import schema, exceptions, service
from monitor.service import create_host_service

router = APIRouter(
    prefix="/api/v1/host",
)


@router.get("/{host_id}", response_model=schema.Host)
def get_host(
        host_id: str,
        host_service: service.HostService = Depends(service.create_host_service),
):
    host = host_service.get_one(host_id)

    if host is None:
        raise exceptions.ResourceNotFoundException(host_id, "host")

    return host


@router.get("", response_model=list[schema.Host], status_code=HTTPStatus.OK)
def get_hosts(host_service: service.HostService = Depends(service.create_host_service)):
    hosts = host_service.get_all()
    return hosts


@router.post("", status_code=HTTPStatus.CREATED)
def create_host(
        host_create: schema.HostCreate,
        host_service: service.HostService = Depends(create_host_service),
):
    host_service.create_host(host_create)
