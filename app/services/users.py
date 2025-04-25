from app.dao.users import insert_user, select_all_users, select_user_by_id, delete_user, update_user
from app.models.users import format_users_from_raw, format_user_from_raw
from app.schemas.users import Users, UsersCreate


async def fetch_all_users() -> list[Users]:
    """
    Affiche les utilisateurs stockés dans la BDD.
    """
    raw_users = select_all_users()
    users = format_users_from_raw(raw_users)
    return users


async def fetch_user_by_id(user_id: str) -> Users:
    """
    Affiche un utilisateur stocké dans la BDD.
    """
    raw_user = select_user_by_id(user_id)
    user = format_user_from_raw(raw_user)
    return user


async def create_user(user: UsersCreate) -> Users:
    """
    Crée un utilisateur dans la BDD.
    """
    raw_user = await insert_user(user)
    user = format_user_from_raw(raw_user)
    return user


async def edit_user(user_id: str, user: Users) -> Users:
    """
    Modifie un utilisateur dans la BDD.
    """
    raw_user = await update_user(user_id, user)
    user = format_user_from_raw(raw_user)
    return user


async def remove_user(user_id: str) -> str:
    """
    Supprime un utilisateur dans la BDD.
    """
    user = await select_user_by_id(user_id)
    if user:
        await delete_user(user_id)
        return f"User {user_id} deleted"
    return f"User {user_id} not found"