from sqlalchemy import Column, Integer, String, Boolean, UniqueConstraint

from monitor.database.db import Base


# class BaseModel(Base):
#     def as_dict(self):
#         result = {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
#         return result
#

class Host(Base):
    __tablename__ = "host"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    ip_address = Column(String, nullable=True)
    enabled = Column(Boolean, default=True, nullable=False)

    UniqueConstraint("name", "ip_address", name="uq_name")
    UniqueConstraint("ip_address", name="uq_ip_address")
