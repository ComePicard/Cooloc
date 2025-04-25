from psycopg2.extras import RealDictRow

from app.schemas.users import Users


def format_user_from_raw(raw_user: RealDictRow) -> Users:
    """
    Formate les utilisateurs bruts en objets Users.
    """
    return Users(**raw_user)


def format_users_from_raw(raw_users: list[RealDictRow]) -> list[Users]:
    """
    Formate les utilisateurs bruts en objets Users.
    """
    return [format_user_from_raw(raw_user) for raw_user in raw_users]