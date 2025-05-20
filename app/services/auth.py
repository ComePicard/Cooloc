from datetime import datetime, timedelta

from jose import jwt

from app.core.config import SettingsAuth
from app.services.users import fetch_user_by_email
from app.utils.security import verify_password


def create_refresh_token(data: dict):
    config = SettingsAuth()
    expire = datetime.utcnow() + timedelta(days=7)
    data.update({"exp": expire})
    return jwt.encode(data, config.SECRET_KEY, algorithm=config.ALGORITHM)


def create_access_token(data: dict):
    config = SettingsAuth()
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=config.EXPIRATION_TIME)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)


async def authenticate_user(email: str, password: str):
    user = await fetch_user_by_email(email)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user
