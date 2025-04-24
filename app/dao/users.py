from fastapi import APIRouter

from app.db.settings import connection_async
from app.schemas.users import Users

router = APIRouter()

async def get_all_users() -> list[Users]:
    """
    Affiche les utilisateurs stockés dans la BDD.
    """
    async with connection_async() as conn:
        async with conn.cursor() as cur:
            sql = "SELECT * FROM Users"
            await cur.execute(sql)
            return [Users(**result) for result in (await cur.fetchall())]


@router.post('/')
async def create_user():
    """
    Crée un utilisateur dans la BDD.
    """
    return {"message": "User created"}