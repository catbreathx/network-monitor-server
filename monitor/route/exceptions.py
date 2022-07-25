from http import HTTPStatus

from starlette.responses import JSONResponse

from monitor.exceptions import exceptions


def create_exception_handlers(app):
    @app.exception_handler(exceptions.ResourceNotFoundException)
    async def resource_not_found_exception_handler(_,
                                                   exception: exceptions.ResourceNotFoundException):
        msg = {
            "message": "Resource Not Found",
            "resource_id": exception.resource_id,
            "resource_type": exception.resource_type,
        }

        return JSONResponse(status_code=HTTPStatus.NOT_FOUND, content=msg)
