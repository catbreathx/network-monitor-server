from pydantic import BaseSettings, PostgresDsn, Field, SecretStr


class Settings(BaseSettings):
    database_url: PostgresDsn = Field(env="DATABASE_URL")
    jwt_private_key: SecretStr = Field(env="JWT_PRIVATE_KEY")
    jwt_public_key: str = Field(env="JWT_PUBLIC_KEY")
    jwt_token_expiration_minutes: int = Field(env="JWT_TOKEN_EXPIRATION_MINUTES")
    jwt_refresh_token_expiration_minutes: int = Field(env="REFRESH_TOKEN_EXPIRE_MINUTES")
    jwt_algorithm: str = Field(env="JWT_ALGORITHM")

    class Config:
        env_file = ".env"


def load_settings(env_file):
    global _settings
    _settings = Settings(_env_file=env_file)


def app_settings() -> Settings:
    global _settings
    return _settings


_settings: Settings
