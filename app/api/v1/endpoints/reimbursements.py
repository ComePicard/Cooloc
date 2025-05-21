from fastapi import APIRouter, Depends

from app.dependencies.auth import get_current_user
from app.schemas.auth import TokenData
from app.schemas.reimbursements import SpendingReimbursement, SpendingReimbursementCreate
from app.services.reimbursements import fetch_reimbursements_by_spending, fetch_reimbursements_by_user, create_reimbursement, \
    remove_reimbursement

router = APIRouter()


@router.get(path="/reimbursements/spending/{spending_id}")
async def get_reimbursements_by_spending(spending_id: str, current_user: TokenData = Depends(get_current_user)) -> list[
    SpendingReimbursement]:
    """
    Affiche les remboursements pour une dépense.
    """
    return await fetch_reimbursements_by_spending(spending_id)


@router.get(path="/reimbursements/user/{user_id}")
async def get_reimbursements_by_user(user_id: str, current_user: TokenData = Depends(get_current_user)) -> list[
    SpendingReimbursement]:
    """
    Affiche les remboursements pour un utilisateur.
    """
    return await fetch_reimbursements_by_user(user_id)


@router.post(path="/reimbursements")
async def post_reimbursement(reimbursement: SpendingReimbursementCreate,
                             current_user: TokenData = Depends(get_current_user)) -> SpendingReimbursement:
    """
    Crée un remboursement dans la BDD.
    """
    return await create_reimbursement(reimbursement)


@router.delete(path="/reimbursements/{spending_id}/{user_id}")
async def delete_reimbursement(spending_id: str, user_id: str,
                               current_user: TokenData = Depends(get_current_user)) -> str:
    """
    Supprime un remboursement de la BDD.
    """
    return await remove_reimbursement(spending_id, user_id)
