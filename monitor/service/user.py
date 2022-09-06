from fastapi import Depends
from sqlalchemy.orm import Session

from monitor import schema
from monitor.repository import get_db_session
from monitor.repository.user import UserRepository


class UserService:
    def __init__(self, db: Session, user_repository: UserRepository):
        self._db: Session = db
        self._user_repository: UserRepository = user_repository

    def create_user(self, user_create: schema.UserCreate) -> schema.user.User:
        try:
            user = self._user_repository.create_user(self._db, user_create)
            self._db.commit()
        except Exception as e:
            self._db.rollback()
            raise e

        return user


def create_user_service(db_session: Session = Depends(get_db_session)) -> UserService:
    service = UserService(db_session, UserRepository())
    return service
