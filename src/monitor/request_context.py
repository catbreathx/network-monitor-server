from starlette_context import context

from monitor.database import models

CURRENT_USER = "current_user"


def get_user_from_context() -> models.User:
    user = context[CURRENT_USER]
    return user


def set_user_in_context(user: models.User) -> None:
    context[CURRENT_USER] = user
