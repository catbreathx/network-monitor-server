from http import HTTPStatus

from fastapi import Depends, APIRouter

from monitor import schema, exceptions, service
from monitor.route import authorization
from monitor.service import create_host_service

router = APIRouter(
    prefix="/api/v1/hosts",
)


@router.get(
    "/{host_id}",
    response_model=schema.Host,
    dependencies=[Depends(authorization.set_current_user_in_context)],
)
def get_one_host(
    host_id: str, host_service: service.HostService = Depends(service.create_host_service)
):
    host = host_service.get_one(host_id)

    if host is None:
        raise exceptions.ResourceNotFoundException(host_id, "host")

    return host


@router.get(
    "",
    response_model=list[schema.Host],
    status_code=HTTPStatus.OK,
    dependencies=[Depends(authorization.set_current_user_in_context)],
)
def get_hosts(
    host_service: service.HostService = Depends(service.create_host_service),
):
    hosts = host_service.get_all()
    return hosts


@router.post(
    "",
    status_code=HTTPStatus.CREATED,
    response_model=schema.HostCreateOut,
    dependencies=[Depends(authorization.set_current_user_in_context)],
)
def create_host(
    host_create: schema.HostCreate,
    host_service: service.HostService = Depends(create_host_service),
):
    new_host = host_service.create_host(host_create)
    return new_host


@router.put(
    "/{host_id}",
    status_code=HTTPStatus.OK,
    response_model=schema.HostCreateOut,
    dependencies=[Depends(authorization.set_current_user_in_context)],
)
def update_host(
    host_id: str,
    host_update: schema.HostUpdate,
    host_service: service.HostService = Depends(create_host_service),
):
    updated_host = host_service.update_host(host_id, host_update)
    return updated_host
