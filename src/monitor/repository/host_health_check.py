from monitor.database import models
from monitor.repository.repository import AbstractBaseRepository


class HostHealthCheckRepository(AbstractBaseRepository):
    _model = models.HostHealthCheck
