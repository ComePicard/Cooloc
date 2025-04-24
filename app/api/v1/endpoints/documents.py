from fastapi import APIRouter

router = APIRouter()

@router.get(path="/")
async def get_documents():
    """
    Affiche les utilisateurs stockés dans la BDD.
    """
    return {"message": "Hello World"}