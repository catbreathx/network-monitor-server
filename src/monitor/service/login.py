from fastapi import Depends
from sqlalchemy.orm import Session

from monitor import schema
from monitor.repository import get_db_session
from monitor.repository.user import UserRepository


class LoginService:
    _user_repository: UserRepository
    _db: Session

    def __init__(self, db: Session, user_repository: UserRepository):
        self._db = db
        self._user_repository = user_repository

    def authenticate_login(self, credentials: schema.Credentials):
        user = self._user_repository.authenticate_user(
            self._db, credentials.email, credentials.password
        )

        return user


def create_login_service(db_session: Session = Depends(get_db_session)) -> LoginService:
    service = LoginService(db_session, UserRepository())
    return service
