import logging
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import JSONResponse

from monitor import schema, service
from monitor.route import jwt_utils
from monitor.settings import app_settings

router = APIRouter(
    prefix="/api/v1/login",
)

logger = logging.getLogger(__name__)


@router.post("", status_code=HTTPStatus.OK)
def login(
    credentials: schema.Credentials,
    login_service: service.LoginService = Depends(service.create_login_service),
):
    logging.debug(f"Logging in user - {credentials.email}")
    user = login_service.authenticate_login(credentials)

    if user is None:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)

    jwt_token = jwt_utils.create_access_token(
        user.email,
        app_settings().jwt_token_expiration_minutes,
        app_settings().jwt_private_key.get_secret_value(),
    )

    headers = {"Authorization": f"Bearer {jwt_token}"}

    return JSONResponse(content={}, headers=headers)
