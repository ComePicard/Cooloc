from app.dao.users import select_all_users
from app.models.users import format_users_from_raw
from app.schemas.users import Users


async def get_all_users() -> list[Users]:
    """
    Affiche les utilisateurs stockés dans la BDD.
    """
    raw_users = select_all_users()
    users = format_users_from_raw(raw_users)
    return users