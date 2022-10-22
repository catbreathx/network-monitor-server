from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette_context import context

from monitor import service, request_context
from monitor.authentication import jwt
from monitor.database import models
from monitor.exceptions import exceptions
from monitor.settings import app_settings


def verify_token(
    header: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    user_service: service.UserService = Depends(service.create_user_service),
) -> models.User:
    jwt_key = app_settings().jwt_public_key
    algorithm = app_settings().jwt_algorithm
    user = jwt.get_user_from_jwt_token(header.credentials, jwt_key, algorithm)
    db_user = user_service.get_user_by_id(user.id)

    if db_user is None:
        raise exceptions.AuthenticationException("User is not authenticated")

    if db_user.is_active is False:
        raise exceptions.AuthenticationException("User is not authenticated")

    return db_user


def set_current_user_in_context(user: models.User = Depends(verify_token)) -> None:
    context[request_context.CURRENT_USER] = user
