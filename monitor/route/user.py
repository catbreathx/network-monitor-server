from http import HTTPStatus

from fastapi import APIRouter, Depends

from monitor import schema, service

router = APIRouter(
    prefix="/api/v1/user",
)


@router.post("", status_code=HTTPStatus.CREATED, response_model=schema.UserCreateOut)
def create_user(
    user_create: schema.UserCreate,
    user_service: service.UserService = Depends(service.create_user_service),
):
    new_user = user_service.create_user(user_create)
    return new_user
