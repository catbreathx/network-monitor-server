import os

from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette_context.middleware import RawContextMiddleware

from monitor import initialize_logging, schema, middleware, route, settings
from monitor.database import db

app_instance: FastAPI

starlette_middleware = [
    Middleware(
        RawContextMiddleware,
    )
]


def bootstrap():
    try:
        initialize_logging()

        settings.load_settings(os.environ["ENV_FILE"])
        db.initialize_database()

        global app_instance
        app_instance = FastAPI(middleware=starlette_middleware)
        schema.init_schema(app_instance)

        middleware.add_middleware(app_instance)
        app_instance.include_router(route.host_router)
        app_instance.include_router(route.user_router)
        app_instance.include_router(route.login_router)
        route.create_exception_handlers(app_instance)
    except Exception as e:
        print(f"Error Could not start up Server {e}")
        exit(1)


bootstrap()
