from passlib.context import CryptContext
from sqlalchemy import Column, Integer, Boolean, UniqueConstraint, Text, inspect
from sqlalchemy.orm import validates

from monitor.database.db import Base
from monitor.database.fields import Password

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AbstractBaseModel(Base):
    __abstract__ = True

    def update_from(self, obj: dict):
        for var, value in obj.items():
            setattr(self, var, value) if value else None

    def json(self) -> dict:
        result = {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

        return result


class Host(AbstractBaseModel):
    __tablename__ = "host"

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    ip_address = Column(Text, nullable=True)
    enabled = Column(Boolean, default=True, nullable=False)

    UniqueConstraint("name", "ip_address", name="uq_name")
    UniqueConstraint("ip_address", name="uq_ip_address")


class User(AbstractBaseModel):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
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
    def validate_password(self, key: str, password):
        validator = getattr(type(self), key).type.validator
        result = validator(password)
        return result

    @property
    def is_active(self) -> bool:
        active = self.account_confirmed is True and self.enabled is True
        return active
