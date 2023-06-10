import logging

from sqlalchemy import select
from sqlalchemy.orm import Session

from monitor import schema
from monitor.database import models
from monitor.exceptions.exceptions import DuplicateUser
from monitor.repository.repository import AbstractBaseRepository

logger = logging.getLogger(__name__)


class UserRepository(AbstractBaseRepository):
    _model = models.User

    def create_resource(
        self,
        session: Session,
        user_create: schema.user.UserCreate,
    ) -> models.AbstractBaseModel:

        existing_user = self.get_by_email(session, user_create.email)

        if existing_user:
            raise DuplicateUser(user_create.email)

        user = models.User(**user_create.dict(exclude={"confirm_password"}))
        session.add(user)

        return user

    def get_by_email(self, session: Session, email: str) -> models.User:
        statement = select(models.User).where(models.User.email == email)
        dataset = session.execute(statement)
        result = dataset.scalar_one_or_none()

        return result

    def authenticate_user(self, session: Session, email: str, password: str) -> models.User | None:
        user: models.User = self.get_by_email(session, email)
        user.enabled
        if user is None:
            logger.info(f"User {email} not found")
            return None

        if user.enabled is False:
            logger.warning(f"User {email} has not been enabled")
            return None

        if user.password != password:
            logger.warning(f"User {email}: incorrect password")
            return None

        logging.info(f"User {email} authenticated.")

        return user
