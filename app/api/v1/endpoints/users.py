from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies.auth import get_current_user
from app.schemas.auth import TokenData
from app.schemas.users import User, UserCreate
from app.services.users import fetch_user_by_id, create_user, edit_user, \
    fetch_user_by_email

router = APIRouter()


@router.get(path="/{user_id}")
async def get_user(user_id: str) -> User:
    """
    Affiche un utilisateur stocké dans la BDD.
    """
    return await fetch_user_by_id(user_id)


@router.get(path="/me")
async def get_my_user(current_user: TokenData = Depends(get_current_user)) -> User:
    """
    Affiche les données de l'utilisateur connecté.
    """
    return await fetch_user_by_id(current_user.id)


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
