from fastapi import FastAPI

from monitor.scheduler import scheduler


def init_events(app: FastAPI):
    @app.on_event("startup")
    async def init_scheduler():
        scheduler.setup_scheduler()

    @app.on_event("shutdown")
    async def shutdown_scheduler():
        scheduler.shutdown_scheduler()
