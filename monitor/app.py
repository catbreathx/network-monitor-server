import os

from fastapi import FastAPI

from monitor import route, middleware, initialize_logging, schema
from monitor.database.db import initialize_database
from monitor.route import create_exception_handlers
from monitor.settings import load_settings

app: FastAPI


def bootstrap():
    try:
        initialize_logging()
        os.getcwd()
        load_settings(os.environ["ENV_FILE"])
        initialize_database()

        global app
        app = FastAPI()
        schema.init_schema(app)

        middleware.add_middleware(app)
        app.include_router(route.host_router)
        app.include_router(route.user_router)
        app.include_router(route.login_router)
        create_exception_handlers(app)
    except Exception as e:
        print(f"Error Could not start up Server {e}")
        exit(1)


bootstrap()
