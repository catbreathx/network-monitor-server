from http import HTTPStatus

from fastapi import FastAPI, Request
from starlette.responses import JSONResponse


def add_middleware(app: FastAPI):
    @app.middleware("http")
    async def exception_observer(request: Request, call_next):
        try:
            response = await call_next(request)
        except Exception as e:
            if e.__class__ == Exception:
                msg = {"message": str(e)}
                return JSONResponse(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, content=msg)

            raise e

        return response
