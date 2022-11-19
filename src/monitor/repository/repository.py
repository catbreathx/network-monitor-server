from abc import ABC

import pydantic
from sqlalchemy import select, update
from sqlalchemy.orm import Session

from monitor.database import models


class AbstractBaseRepository(ABC):
    _model: type[models.AbstractBaseModel]

    @property
    def model(self) -> type[models.AbstractBaseModel]:
        return self._model

    def get_all(self, session: Session) -> models.AbstractBaseModel:
        statement = select(self.model)
        result = session.execute(statement)
        hosts = result.scalars().all()

        return hosts

    def get_one(self, session: Session, resource_id: int) -> models.AbstractBaseModel:
        statement = select(self.model).where(self.model.id == resource_id)
        dataset = session.execute(statement)
        result = dataset.scalar_one_or_none()

        return result

    def create_resource(
        self, session: Session, schema_create: pydantic.BaseModel
    ) -> models.AbstractBaseModel:
        resource = self.model(**schema_create.dict())
        session.add(resource)
        session.flush()
        return resource

    def update_resource(
        self, session: Session, resource: models.AbstractBaseModel
    ) -> models.AbstractBaseModel:
        statement = update(self.model).where(self.model.id == resource.id).values(resource.json())
        session.execute(statement)
        session.commit()

        return resource
