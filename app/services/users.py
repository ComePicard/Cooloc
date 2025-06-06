from app.dao.users import insert_user, select_user_by_id, select_user_by_email, \
    update_user
from app.models.users import format_user_from_raw
from app.schemas.users import User, UserCreate
from app.utils.security import get_password_hash


async def fetch_user_by_id(user_id: str) -> User:
    """
    Affiche un utilisateur stocké dans la BDD.
    """
    raw_user = await select_user_by_id(user_id)
    user = format_user_from_raw(raw_user)
    return user


async def fetch_user_by_email(email: str) -> User:
    """
    Affiche un utilisateur stocké dans la BDD.
    """
    raw_user = await select_user_by_email(email)
    user = format_user_from_raw(raw_user)
    return user


async def create_user(user: UserCreate) -> User:
    """
    Crée un utilisateur dans la BDD.
    """
    # Create a copy of the user to avoid modifying the original
    user_dict = user.model_dump()
    # Hash the password
    password = user.password.get_secret_value()
    user_dict["password"] = get_password_hash(password)
    # Create a new UserCreate object with the hashed password
    user_with_hashed_password = UserCreate(**user_dict)
    # Insert the user with the hashed password
    raw_user = await insert_user(user_with_hashed_password)
    user = format_user_from_raw(raw_user)
    return user


async def edit_user(user_id: str, user: UserCreate) -> User:
    """
    Modifie un utilisateur dans la BDD.
    """
    # Create a copy of the user to avoid modifying the original
    user_dict = user.model_dump()
    # Hash the password
    password = user.password.get_secret_value()
    user_dict["password"] = get_password_hash(password)
    # Create a new UserCreate object with the hashed password
    user_with_hashed_password = UserCreate(**user_dict)
    # Update the user with the hashed password
    raw_user = await update_user(user_id, user_with_hashed_password)
    user = format_user_from_raw(raw_user)
    return user
