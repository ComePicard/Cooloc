from fastapi import APIRouter, Depends

from app.dependencies.auth import get_current_user
from app.schemas.auth import TokenData
from app.schemas.spendings import Spending, SpendingCreate
from app.services.spendings import fetch_spendings_by_group, fetch_spending_by_id, create_spending, edit_spending, \
    fetch_spendings_by_user_id

router = APIRouter()


@router.get(path="/{spending_id}")
async def get_spending_by_id(spending_id: int, current_user: TokenData = Depends(get_current_user)) -> Spending:
    """
    Affiche une dépense stockée dans la BDD.
    """
    return await fetch_spending_by_id(spending_id)


@router.get(path="/me")
async def get_my_spendings(current_user: TokenData = Depends(get_current_user)) -> list[Spending]:
    """
    Affiche la/les dépense(s) de l'utilisateur connecté.
    """
    return await fetch_spendings_by_user_id(current_user)


@router.get(path="/group/{group_id}")
async def get_spendings_by_group(group_id: str, current_user: TokenData = Depends(get_current_user)) -> list[Spending]:
    """
    Affiche les dépenses stockées par groupe dans la BDD.
    """
    return await fetch_spendings_by_group(group_id)


@router.post(path="/")
async def post_spending(spending: SpendingCreate, current_user: TokenData = Depends(get_current_user)) -> Spending:
    """
    Crée une dépense dans la BDD.
    """
    return await create_spending(spending, current_user)


@router.patch(path="/{spending_id}")
async def patch_spending(spending_id: str, spending: SpendingCreate,
                         current_user: TokenData = Depends(get_current_user)) -> Spending:
    """
    Modifie une dépense dans la BDD.
    """
    return await edit_spending(spending_id, spending)
