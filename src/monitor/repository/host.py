from sqlalchemy import select, update
from sqlalchemy.orm import Session

from monitor import schema
from monitor.database import models


class HostRepository:
    def get_all(self, session: Session):
        statement = select(models.Host)
        result = session.execute(statement)
        hosts = result.scalars().all()
        return hosts

    def get_one(self, session: Session, host_id) -> models.Host:
        statement = select(models.Host).where(models.Host.id == host_id)
        dataset = session.execute(statement)
        result = dataset.scalar_one_or_none()

        return result

    def create_host(self, session: Session, host_create: schema.host.HostCreate) -> models.Host:
        host = models.Host(**host_create.dict())
        session.add(host)

        return host

    def update_host(self, session: Session, host: models.Host) -> models.Host:
        statement = update(models.Host).where(models.Host.id == host.id).values(host.json())
        session.execute(statement)
        session.commit()

        return host
