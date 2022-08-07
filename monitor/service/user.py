from fastapi import Depends
from sqlalchemy.orm import Session

from monitor import schema
from monitor.repository import get_db_session
from monitor.repository.user import UserRepository


class UserService:
    def __init__(self, db: Session, user_repository: UserRepository):
        self._db = db
        self._user_repository = user_repository

    def create_user(self, user: schema.UserCreate) -> schema.User:
        pass


def create_user_service(db_session: Session = Depends(get_db_session)) -> UserService:
    service = UserService(db_session, UserRepository())
    return service
