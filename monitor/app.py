from fastapi import FastAPI

from monitor import route
from monitor import schema, load_settings
from monitor.database.db import initialize_database
from monitor.route import create_exception_handlers

load_settings()
initialize_database()
app = FastAPI()
app.include_router(route.host_router)
create_exception_handlers(app)
schema.init_schema(app)
