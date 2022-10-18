from http import HTTPStatus

from fastapi import APIRouter, Depends

from monitor import schema, service
from monitor.route import authorization

router = APIRouter(
    prefix="/api/v1/users",
)


@router.post(
    "",
    status_code=HTTPStatus.CREATED,
    response_model=schema.UserCreateOut,
    dependencies=[Depends(authorization.set_current_user_in_context)],
)
def create_user(
    user_create: schema.UserCreate,
    user_service: service.UserService = Depends(service.create_user_service),
):
    new_user = user_service.create_user(user_create)
    return new_user


@router.get(
    "/{resource_id}",
    status_code=HTTPStatus.OK,
    response_model=schema.User,
    dependencies=[Depends(authorization.set_current_user_in_context)],
)
def get_one_user(
    resource_id: int,
    user_service: service.UserService = Depends(service.create_user_service),
):
    user = user_service.get_user_by_id(resource_id)
    return user
