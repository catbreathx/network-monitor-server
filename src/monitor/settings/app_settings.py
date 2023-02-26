from typing import Optional

from pydantic import BaseSettings, Field, SecretStr


class Settings(BaseSettings):
    database_url: str = Field(env="DATABASE_URL")
    jwt_private_key: SecretStr = Field(env="JWT_PRIVATE_KEY")
    jwt_public_key: str = Field(env="JWT_PUBLIC_KEY")
    jwt_token_expiration_minutes: int = Field(env="JWT_TOKEN_EXPIRATION_MINUTES")
    jwt_refresh_token_expiration_minutes: int = Field(env="REFRESH_TOKEN_EXPIRE_MINUTES")
    jwt_algorithm: str = Field(env="JWT_ALGORITHM")
    scheduler_enabled: Optional[bool] = Field(env="SCHEDULER_ENABLED", default=True)
    email_username: str = Field(env="MAIL_USERNAME")
    email_password: str = Field(env="MAIL_PASSWORD")
    email_server: str = Field(env="MAIL_SERVER")
    email_template_directory: str = Field(env="TEMPLATE_FOLDER")
    email_port: int = Field(env="MAIL_PORT")
    email_starttls: bool = Field(env="MAIL_STARTTLS", default=True)
    email_ssl_tls: bool = Field(env="MAIL_SSL_TLS", default=True)
    mail_from: str = Field(env="MAIL_FROM")

    class Config:
        env_file = ".env"


def load_settings(env_file):
    global _settings
    _settings = Settings(_env_file=env_file)


def app_settings() -> Settings:
    global _settings
    return _settings


_settings: Settings
