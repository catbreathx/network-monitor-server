import datetime
from typing import List, Optional

from passlib.context import CryptContext
from sqlalchemy import (
    JSON,
    TIMESTAMP,
    Boolean,
    ForeignKey,
    Integer,
    Text,
    UniqueConstraint,
    func,
    inspect,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from monitor.database import utils
from monitor.database.db import Base
from monitor.database.fields import Password

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AbstractBaseModel(Base):
    __abstract__ = True
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    def update_from(self, obj: dict):
        for var, value in obj.items():
            setattr(self, var, value) if value else None

    def json(self) -> dict:
        result = {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

        return result


class Host(AbstractBaseModel):
    __tablename__ = "host"

    name: Mapped[str] = mapped_column(nullable=False)
    ip_address: Mapped[str] = mapped_column(Text, nullable=True)
    enabled: Mapped[bool] = mapped_column(default=True, nullable=False)

    UniqueConstraint("name", "ip_address", name="uq_name")
    UniqueConstraint("ip_address", name="uq_ip_address")


class User(AbstractBaseModel):
    __tablename__ = "user"

    type_annotation_map = {}

    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[Optional[str]] = mapped_column(nullable=True)
    email: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(Password, nullable=False)
    enabled: Mapped[bool] = mapped_column(default=True, nullable=False)
    account_confirmed: Mapped[bool] = mapped_column(default=False, nullable=False)
    password_change_token: Mapped[Optional[str]] = mapped_column(nullable=True)

    UniqueConstraint("email", name="uq_email")

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @validates("password")
    def validate_password(self, key: str, password: str) -> utils.PasswordHash:
        validator = getattr(type(self), key).type.validator
        result = validator(password)
        return result

    @property
    def is_active(self) -> bool:
        active = self.account_confirmed is True and self.enabled is True
        return active


class ScheduledJob(AbstractBaseModel):
    __tablename__ = "scheduled_job"

    data: Mapped[Optional[JSON]] = mapped_column(JSON, nullable=True)
    job: Mapped[str] = mapped_column(Text, nullable=False)
    triggered_by: Mapped[str] = mapped_column(Text, nullable=False)
    date_time: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    host_health_checks: Mapped[List["HostHealthCheck"]] = relationship(
        "HostHealthCheck", back_populates="scheduled_job"
    )


class HostHealthCheck(AbstractBaseModel):
    __tablename__ = "host_health_check"

    is_reachable: Mapped[bool] = mapped_column(Boolean, nullable=False)
    output_text: Mapped[bool] = mapped_column(Text, nullable=False)
    host_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(f"{Host.__tablename__}.id"), nullable=False
    )
    scheduled_job = relationship("ScheduledJob", back_populates="host_health_checks")

    scheduled_job_id = mapped_column(
        Integer, ForeignKey(f"{ScheduledJob.__tablename__}.id"), nullable=False
    )
