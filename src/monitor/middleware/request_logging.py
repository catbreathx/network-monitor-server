import logging

from fastapi import FastAPI, Request
from starlette.responses import Response

logger = logging.getLogger(__name__)


def add_middleware(app: FastAPI):
    @app.middleware("http")
    async def request_logging(request: Request, call_next) -> Response:
        logger.info(f"Request {request.url} starting...")
        response: Response = await call_next(request)
        logger.info(f"Request {request.url} finished, response status {response.status_code}")

        return response
