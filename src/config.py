from pydantic import PostgresDsn
from pydantic_settings import SettingsConfigDict, BaseSettings

class DBSettings(BaseSettings):
    user: str
    password: str
    host: str
    port: int
    name: str
    url: PostgresDsn

    model_config = SettingsConfigDict(
        env_prefix="db_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

class AuthSettings(BaseSettings):
    secret_key: str
    algorithm: str
    token_time_minutes_expiration: int

    model_config = SettingsConfigDict(
        env_prefix="auth_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

db_settings = DBSettings()
auth_settings = AuthSettings()