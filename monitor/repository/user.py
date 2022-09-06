import logging

from sqlalchemy import select
from sqlalchemy.orm import Session

from monitor import schema
from monitor.database import models

logger = logging.getLogger(__name__)


class UserRepository:
    def get_all(self, session: Session):
        statement = select(models.User)
        result = session.execute(statement)
        hosts = result.scalars().all()
        return hosts

    def create_user(self, session: Session, user_create: schema.user.UserCreate) -> models.User:
        user = models.User(**user_create.dict(exclude={"confirm_password"}))
        session.add(user)

        return user

    def get_one(self, session: Session, user_id: int) -> models.User:
        statement = select(models.User).where(models.User.id == user_id)
        dataset = session.execute(statement)
        result = dataset.scalar_one_or_none()

        return result

    def get_by_email(self, session: Session, email: str) -> models.User:
        statement = select(models.User).where(models.User.email == email)
        dataset = session.execute(statement)
        result = dataset.scalar_one_or_none()

        return result

    def authenticate_user(self, session: Session, email: str, password: str) -> [models.User, None]:
        user: models.User = self.get_by_email(session, email)
        is_authenticated = False

        if user is None:
            logger.info(f"User {email} not found")
            return None

        if user.enabled is False:
            logger.warning(f"User {email} has not been enabled")
            return None

        if user.password != password:
            logger.warning(f"User {email}: incorrect password")
            return None

        logging.info(f"User {email} is authenticated = {is_authenticated}")

        return user
