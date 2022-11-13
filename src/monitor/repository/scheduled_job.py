from monitor.database import models
from monitor.repository.repository import AbstractBaseRepository


class ScheduledJobRepository(AbstractBaseRepository):
    _model = models.ScheduledJob
