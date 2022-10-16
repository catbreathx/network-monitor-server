from http import HTTPStatus

from fastapi import APIRouter, Depends

from monitor import schema, service
from monitor.route import authorization

router = APIRouter(
    prefix="/api/v1/user",
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
