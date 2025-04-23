import psycopg2
from psycopg2 import OperationalError
from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    POSTGRESQL_USER: str
    POSTGRESQL_PASSWORD: SecretStr
    POSTGRESQL_HOST: str
    POSTGRESQL_PORT: str


def create_postgres_connection(host, database, user, password, port=5432):
    try:
        connection = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port
        )
        print("Connexion réussie à PostgreSQL")
        return connection
    except OperationalError as e:
        print(f"Erreur lors de la connexion à PostgreSQL : {e}")
        return None


settings = Settings()
