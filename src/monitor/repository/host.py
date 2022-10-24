from monitor.database import models
from monitor.repository.repository import AbstractBaseRepository


class HostRepository(AbstractBaseRepository):
    _model = models.Host
