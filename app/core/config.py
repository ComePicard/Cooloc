from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRESQL_USER: str
    POSTGRESQL_PASSWORD: SecretStr
    POSTGRESQL_HOST: str
    POSTGRESQL_PORT: str


settings = Settings()
