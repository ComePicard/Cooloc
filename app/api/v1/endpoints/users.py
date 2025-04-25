from fastapi import APIRouter

from app.dao.users import create_user
from app.schemas.users import Users, UsersCreate
from app.services.users import get_all_users

router = APIRouter()

@router.get(path="/")
async def get_users() -> list[Users]:
    """
    Affiche les utilisateurs stockés dans la BDD.
    """
    return await get_all_users()


@router.post('/')
async def post_user(user: UsersCreate) -> Users:
    """
    Crée un utilisateur dans la BDD.
    """
    result = await create_user(user)
    return Users(**result)