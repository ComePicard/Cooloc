from passlib.context import CryptContext
from pydantic import SecretStr

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: SecretStr):
    return pwd_context.verify(plain_password, hashed_password.get_secret_value())


def get_password_hash(password):
    return pwd_context.hash(password)
