from pydantic import BaseSettings, PostgresDsn, Field, SecretStr


class Settings(BaseSettings):
    database_url: PostgresDsn = Field(env="DATABASE_URL")
    secret_key: SecretStr = Field(env="SECRET_KEY")
    jwt_token_expiration_minutes: int = Field(env="JWT_TOKEN_EXPIRATION_MINUTES")

    class Config:
        env_file = ".env"


app_settings: Settings


def load_settings(env_file):
    global app_settings
    app_settings = Settings(_env_file=env_file)


def get_app_settings():
    global app_settings
    return app_settings
