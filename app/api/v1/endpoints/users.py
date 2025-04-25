from fastapi import APIRouter

from app.dao.users import get_all_users, create_user
from app.schemas.users import Users, UsersCreate

router = APIRouter()

@router.get(path="/")
async def get_users() -> list[Users]:
    """
    Affiche les utilisateurs stockés dans la BDD.
    """
    results = await get_all_users()
    users = [Users(**result) for result in results]
    return users


@router.post('/')
async def post_user(user: UsersCreate) -> Users:
    """
    Crée un utilisateur dans la BDD.
    """
    result = await create_user(user)
    return Users(**result)