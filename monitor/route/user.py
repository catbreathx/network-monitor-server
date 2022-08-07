from http import HTTPStatus

from fastapi import APIRouter, Depends

from monitor import schema, service

router = APIRouter(
    prefix="/api/v1/user",
)


@router.post("", response_model=schema.UserCreate, status_code=HTTPStatus.OK)
def create_user(
    user_create: schema.UserCreate,
    user_service: service.UserService = Depends(service.create_user_service),
):
    user_service.create_user(user_create)
