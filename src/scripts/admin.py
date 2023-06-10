import os

import click

from monitor import schema, settings
from monitor.database import db
from monitor.repository import UserRepository
from monitor.service import UserService


@click.command()
@click.option("--email", required=True, type=click.STRING)
@click.option("--password", required=True, type=click.STRING)
@click.option("--first-name", required=True, type=click.STRING)
@click.option("--last-name", required=False, type=click.STRING)
@click.option("--config-file", required=True, type=click.STRING)
def create_user(email: str, password: str, first_name: str, last_name: str, config_file: str):
    os.environ["ENV_FILE"] = config_file
    settings.load_settings(os.environ["ENV_FILE"])
    db.initialize_database()
    db.test_database()

    user = schema.user.UserCreate(
        email=email,
        first_name=first_name,
        last_name=last_name,
        password=password,
        confirm_password=password,
    )

    user_repository = UserRepository()
    user_service = UserService(db.get_session(), user_repository)
    new_user = user_service.create_user(user)

    new_user.account_confirmed = True
    new_user.enabled = True
    new_user.save()

    click.echo(f"Created User - User ID {new_user.id}")


if __name__ == "__main__":
    create_user()
