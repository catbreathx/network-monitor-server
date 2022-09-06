from typing import Optional

from fastapi import Depends
from sqlalchemy.orm import Session

from monitor import schema
from monitor.database import models
from monitor.repository import get_db_session
from monitor.repository.host import HostRepository


class HostService:
    _host_repository: HostRepository
    _db: Session

    def __init__(self, db: Session, host_repository: HostRepository):
        self._db = db
        self._host_repository = host_repository

    def get_all(self) -> list[schema.Host]:
        hosts = self._host_repository.get_all(self._db)

        return hosts

    def create_host(self, host_create: schema.HostCreate) -> models.Host:
        try:
            host = self._host_repository.create_host(self._db, host_create)
            self._db.commit()
        except Exception as e:
            self._db.rollback()
            raise e

        return host

    def get_one(self, host_id: str) -> Optional[models.Host]:
        host = self._host_repository.get_one(self._db, host_id)
        return host


def create_host_service(db_session: Session = Depends(get_db_session)) -> HostService:
    service = HostService(db_session, HostRepository())
    return service
