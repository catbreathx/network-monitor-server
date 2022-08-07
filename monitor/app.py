from fastapi import FastAPI

from monitor import route, middleware
from monitor import schema, load_settings
from monitor.database.db import initialize_database
from monitor.route import create_exception_handlers

app: FastAPI


def bootstrap():
    load_settings()
    initialize_database()
    global app
    app = FastAPI()
    middleware.add_middleware(app)
    app.include_router(route.host_router)
    app.include_router(route.user_router)
    create_exception_handlers(app)
    schema.init_schema(app)


bootstrap()
