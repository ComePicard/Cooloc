from fastapi import APIRouter

router = APIRouter()

@router.get(path="/")
async def get_users():
    """
    Affiche les utilisateurs stockés dans la BDD.
    """
    return {"message": "Hello World"}


@router.post('/')
async def create_user():
    """
    Crée un utilisateur dans la BDD.
    """
    return {"message": "User created"}