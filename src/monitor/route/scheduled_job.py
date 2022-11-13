import logging
from http import HTTPStatus

from fastapi import APIRouter, Depends

from monitor import request_context, schema, service
from monitor.database import models
from monitor.route import authorization
from monitor.service.ping import create_ping_service

router = APIRouter(
    prefix="/api/v1/scheduledjob",
)

logger = logging.getLogger(__name__)


@router.post(
    "/ping",
    status_code=HTTPStatus.CREATED,
    response_model=schema.ScheduledJobOut,
    dependencies=[Depends(authorization.set_current_user_in_context)],
)
def run_scheduled_job(
    ping_service: service.PingService = Depends(create_ping_service),
):
    user: models.User = request_context.get_user_from_context()
    logger.debug(f"Ping scheduled job triggered manually by {user.email}")
    ping_scheduled_job = ping_service.run_scheduled_job(triggered_by=user.full_name)

    return ping_scheduled_job
