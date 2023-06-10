import logging
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import HTMLResponse, RedirectResponse

from monitor import schema, service
from monitor.authentication import jwt
from monitor.settings import app_settings

router = APIRouter(
    prefix="/auth/v1/login",
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
        logging.info(f"Incorrect credentials {credentials}")
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)

    private_key = app_settings().jwt_private_key.get_secret_value()

    jwt_token = jwt.create_jwt_token(
        user,
        app_settings().jwt_token_expiration_minutes,
        app_settings().jwt_private_key.get_secret_value(),
        app_settings().jwt_algorithm,
    )

    refresh_token = jwt.create_refresh_token(
        user.email, secret_key=private_key, algorithm=app_settings().jwt_algorithm
    )

    logger.info(f"User {user.email} logged in.")

    return {"access_token": jwt_token, "refresh_token": refresh_token}


@router.get("", status_code=HTTPStatus.OK, response_class=HTMLResponse)
def logout():
    response = RedirectResponse(url="/")
    return response
