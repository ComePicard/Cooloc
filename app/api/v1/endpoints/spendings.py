from fastapi import APIRouter

from app.schemas.spendings import Spending, SpendingCreate
from app.services.spendings import fetch_spendings_by_group, fetch_spending_by_id, create_spending, edit_spending, \
    remove_spending

router = APIRouter()


@router.get(path="/{spending_id}")
async def get_spending_by_id(spending_id: int) -> Spending:
    """
    Affiche un spending stocké dans la BDD.
    """
    return fetch_spending_by_id(spending_id)


@router.get(path="/{group_id}")
async def get_spendings_by_group(group_id: str) -> list[Spending]:
    """
    Affiche les utilisateurs stockés dans la BDD.
    """
    return fetch_spendings_by_group(group_id)


@router.get(path="/{user_id}")
async def get_spendings_by_user(user_id: str) -> list[Spending]:
    """
    Affiche les utilisateurs stockés dans la BDD.
    """
    return fetch_spendings_by_group(user_id)


@router.post(path="/")
async def post_spending(spending: SpendingCreate) -> Spending:
    """
    Crée un spending dans la BDD.
    """
    return await create_spending(spending)


@router.patch(path="/{spending_id}")
async def patch_spending(spending_id: int, spending: SpendingCreate) -> Spending:
    """
    Modifie un spending dans la BDD.
    """
    return await edit_spending(spending_id, spending)


@router.delete(path="/{spending_id}")
async def delete_spending(spending_id: int) -> str:
    """
    Supprime un spending dans la BDD.
    """
    return await remove_spending(spending_id)