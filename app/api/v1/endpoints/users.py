from fastapi import APIRouter

from app.schemas.users import User, UserCreate
from app.services.users import fetch_all_users, remove_user, fetch_user_by_id, create_user, edit_user

router = APIRouter()


@router.get(path="/")
async def get_users() -> list[User]:
    """
    Affiche les utilisateurs stockés dans la BDD.
    """
    return await fetch_all_users()

@router.get(path="/{user_id}")
async def get_user(user_id: str) -> User:
    """
    Affiche un utilisateur stocké dans la BDD.
    """
    return await fetch_user_by_id(user_id)


@router.post('/')
async def post_user(user: UserCreate) -> User:
    """
    Crée un utilisateur dans la BDD.
    """
    return await create_user(user)

@router.patch('/{user_id}')
async def patch_user(user_id: str, user: UserCreate) -> User:
    """
    Modifie un utilisateur dans la BDD.
    """
    return await edit_user(user_id, user)


@router.delete('/{user_id}')
async def delete_user(user_id: str) -> str:
    """
    Supprime un utilisateur dans la BDD.
    """
    return await remove_user(user_id)