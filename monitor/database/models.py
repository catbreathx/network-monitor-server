from passlib.context import CryptContext
from sqlalchemy import Column, Integer, Boolean, UniqueConstraint, Text

from monitor.database.db import Base

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Host(Base):
    __tablename__ = "host"

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    ip_address = Column(Text, nullable=True)
    enabled = Column(Boolean, default=True, nullable=False)

    UniqueConstraint("name", "ip_address", name="uq_name")
    UniqueConstraint("ip_address", name="uq_ip_address")


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    first_name = Column(Text, nullable=False)
    last_name = Column(Text, nullable=True)
    email = Column(Text, nullable=False)
    password = Column(Text, nullable=False)
    enabled = Column(Boolean, default=True, nullable=False)
    account_confirmed = Column(Boolean, default=False, nullable=False)
    password_change_token = Column(Text, nullable=True)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def set_password(self, plain_password: str) -> None:
        """
        Hash + salt the plain text password and set the password attribute
        :param plain_password: the plain text password
        :return: None
        """
        hashed = password_context.hash(plain_password)

        self.password = hashed

    def verify_password(self, plain_password: str) -> bool:
        result = password_context.verify(plain_password, self.password)
        return result
