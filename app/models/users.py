from psycopg2.extras import RealDictRow

from app.schemas.users import User


def format_user_from_raw(raw_user: RealDictRow) -> User:
    """
    Formate les utilisateurs bruts en objets User.
    """
    return User(**raw_user) if raw_user else None


def format_users_from_raw(raw_users: list[RealDictRow]) -> list[User]:
    """
    Formate les utilisateurs bruts en objets User.
    """
    return [format_user_from_raw(raw_user) for raw_user in raw_users]
