from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    USER: str
    PASSWORD: SecretStr
    HOST: str
    PORT: str
    DB_NAME: str

    class Config:
        env_prefix = 'POSTGRES_'


class SettingsAuth(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    EXPIRATION_TIME: int

    class Config:
        env_prefix = 'JWT_'


settings = Settings()
