from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies.auth import get_current_user
from app.schemas.auth import TokenData
from app.schemas.users import User, UserCreate
from app.services.users import fetch_all_users, remove_user, fetch_user_by_id, create_user, edit_user, fetch_user_by_email

router = APIRouter()


@router.get(path="/")
async def get_users(current_user: TokenData = Depends(get_current_user)) -> list[User]:
    """
    Affiche les utilisateurs stockés dans la BDD.
    """
    return await fetch_all_users()

@router.get(path="/{user_id}")
async def get_user(user_id: str, current_user: TokenData = Depends(get_current_user)) -> User:
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
async def patch_user(user_id: str, user: UserCreate, current_user: TokenData = Depends(get_current_user)) -> User:
    """
    Modifie un utilisateur dans la BDD.
    """
    return await edit_user(user_id, user)


@router.delete('/{user_id}')
async def delete_user(user_id: str, current_user: TokenData = Depends(get_current_user)) -> str:
    """
    Supprime un utilisateur dans la BDD.
    """
    return await remove_user(user_id)


@router.get('/email/{email}')
async def get_user_by_email(email: str, current_user: TokenData = Depends(get_current_user)) -> User:
    """
    Récupère un utilisateur par son email.
    """
    user = await fetch_user_by_email(email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with email {email} not found"
        )
    return user
