from passlib.context import CryptContext
from sqlalchemy import (
    JSON,
    TIMESTAMP,
    Boolean,
    Column,
    ForeignKey,
    Integer,
    Text,
    UniqueConstraint,
    func,
    inspect,
)
from sqlalchemy.orm import validates

from monitor.database import utils
from monitor.database.db import Base
from monitor.database.fields import Password

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AbstractBaseModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True)

    def update_from(self, obj: dict):
        for var, value in obj.items():
            setattr(self, var, value) if value else None

    def json(self) -> dict:
        result = {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

        return result


class Host(AbstractBaseModel):
    __tablename__ = "host"

    name = Column(Text, nullable=False)
    ip_address = Column(Text, nullable=True)
    enabled = Column(Boolean, default=True, nullable=False)

    UniqueConstraint("name", "ip_address", name="uq_name")
    UniqueConstraint("ip_address", name="uq_ip_address")


class User(AbstractBaseModel):
    __tablename__ = "user"

    first_name = Column(Text, nullable=False)
    last_name = Column(Text, nullable=True)
    email = Column(Text, nullable=False)
    password = Column(Password, nullable=False)
    enabled = Column(Boolean, default=True, nullable=False)
    account_confirmed = Column(Boolean, default=False, nullable=False)
    password_change_token = Column(Text, nullable=True)

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

    data = Column(JSON, nullable=True)
    job = Column(Text, nullable=False)
    triggered_by = Column(Text, nullable=False)
    date_time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())


class HostHealthCheck(AbstractBaseModel):
    __tablename__ = "host_health_check"

    is_reachable = Column(Boolean, nullable=False)
    output_text = Column(Text, nullable=False)
    host_id = Column(Integer, ForeignKey(f"{Host.__tablename__}.id"), nullable=False)

    scheduled_job_id = Column(
        Integer, ForeignKey(f"{ScheduledJob.__tablename__}.id"), nullable=False
    )
