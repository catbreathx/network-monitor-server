from http import HTTPStatus

from fastapi import FastAPI
from starlette.responses import JSONResponse

from monitor import exceptions


def create_exception_handlers(app: FastAPI):
    @app.exception_handler(exceptions.ResourceNotFoundException)
    async def resource_not_found_exception_handler(
        _, exception: exceptions.ResourceNotFoundException
    ):
        msg = {
            "message": "Resource Not Found",
            "resource_id": exception.resource_id,
            "resource_type": exception.resource_type,
        }

        return JSONResponse(status_code=HTTPStatus.NOT_FOUND, content=msg)

    @app.exception_handler(exceptions.AuthenticationException)
    async def authentication_error_exception_handler(_, __):
        return JSONResponse(status_code=HTTPStatus.FORBIDDEN, content={})
