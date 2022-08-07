from sqlalchemy import select
from sqlalchemy.orm import Session

from monitor import schema
from monitor.database import models


class UserRepository:
    def get_all(self, session: Session):
        statement = select(models.Host)
        result = session.execute(statement)
        hosts = result.scalars().all()
        return hosts

    def create_host(self, session: Session, host_create: schema.host.HostCreate) -> models.Host:
        host = models.Host(**host_create.dict())
        session.add(host)

        return host

    def get_one(self, session: Session, host_id) -> models.Host:
        statement = select(models.Host).where(models.Host.id == host_id)
        dataset = session.execute(statement)
        result = dataset.scalar_one_or_none()

        return result
