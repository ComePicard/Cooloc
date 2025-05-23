from fastapi import APIRouter, Depends

from app.dependencies.auth import get_current_user
from app.schemas.auth import TokenData
from app.schemas.reimbursements import SpendingReimbursement, SpendingReimbursementCreate, ReimbursementSummary
from app.services.reimbursements import (
    fetch_reimbursements_by_spending, fetch_reimbursements_by_user,
    create_reimbursement, remove_reimbursement,
    fetch_total_reimbursements_owed_by_user, fetch_total_reimbursements_owed_to_user,
    fetch_reimbursement_summary
)

router = APIRouter()


@router.get(path="/spending/{spending_id}")
async def get_reimbursements_by_spending(spending_id: str) -> list[
    SpendingReimbursement]:
    """
    Affiche les remboursements pour une dépense.
    """
    return await fetch_reimbursements_by_spending(spending_id)


@router.get(path="/me")
async def get_my_reimbursements_by_user(current_user: TokenData = Depends(get_current_user)) -> list[
    SpendingReimbursement]:
    """
    Affiche ses remboursements.
    """
    return await fetch_reimbursements_by_user(current_user)

@router.get(path="/me/unpaid")
async def get_my_unpaid_reimbursements(current_user: TokenData = Depends(get_current_user)) -> list[SpendingReimbursement]:
    """
    Récupère tous les remboursements non payés pour l'utilisateur courant.
    """
    from app.services.reimbursements import fetch_unpaid_reimbursements_by_user
    return await fetch_unpaid_reimbursements_by_user(current_user)


@router.patch(path="/{spending_id}/{user_id}/pay")
async def pay_reimbursement(spending_id: str, user_id: str, current_user: TokenData = Depends(get_current_user)):
    """
    Marque un remboursement comme payé (ajoute une date de paiement).
    """
    from datetime import datetime, timezone
    from app.services.reimbursements import mark_reimbursement_as_paid
    await mark_reimbursement_as_paid(spending_id, user_id, datetime.now(timezone.utc))
    return {"status": "paid"}


@router.delete(path="/{spending_id}/{user_id}")
async def delete_reimbursement(spending_id: str, user_id: str,) -> str:
    """
    Supprime un remboursement de la BDD.
    """
    return await remove_reimbursement(spending_id, user_id)


@router.get(path="/me/total-owed-by")
async def get_total_reimbursements_owed_by_user(current_user: TokenData = Depends(get_current_user)) -> float:
    """
    Calcule le montant total des remboursements dus par l'utilisateur courant.
    """
    return await fetch_total_reimbursements_owed_by_user(current_user.id)


@router.get(path="/me/total-owed-to")
async def get_total_reimbursements_owed_to_user(current_user: TokenData = Depends(get_current_user)) -> float:
    """
    Calcule le montant total des remboursements dus à l'utilisateur courant.
    """
    return await fetch_total_reimbursements_owed_to_user(current_user.id)


@router.get(path="/user/{user_id}/total-owed-by")
async def get_total_reimbursements_owed_by_specific_user(user_id: str) -> float:
    """
    Calcule le montant total des remboursements dus par un utilisateur spécifique.
    """
    return await fetch_total_reimbursements_owed_by_user(user_id)


@router.get(path="/user/{user_id}/total-owed-to")
async def get_total_reimbursements_owed_to_specific_user(
        user_id: str, current_user: TokenData = Depends(get_current_user)
) -> float:
    """
    Calcule le montant total des remboursements dus à un utilisateur spécifique.
    """
    return await fetch_total_reimbursements_owed_to_user(user_id)


@router.get(path="/me/summary")
async def get_reimbursement_summary(current_user: TokenData = Depends(get_current_user)) -> ReimbursementSummary:
    """
    Calcule le résumé des remboursements pour l'utilisateur courant.
    Inclut le montant total dû par l'utilisateur, le montant total dû à l'utilisateur,
    et le solde net (positif si l'utilisateur est créditeur, négatif s'il est débiteur).
    """
    summary = await fetch_reimbursement_summary(current_user)
    return ReimbursementSummary(**summary)


@router.get(path="/user/{user_id}/summary")
async def get_reimbursement_summary_for_specific_user(
        user_id: str, current_user: TokenData = Depends(get_current_user)
) -> ReimbursementSummary:
    """
    Calcule le résumé des remboursements pour un utilisateur spécifique.
    Inclut le montant total dû par l'utilisateur, le montant total dû à l'utilisateur,
    et le solde net (positif si l'utilisateur est créditeur, négatif s'il est débiteur).
    """
    summary = await fetch_reimbursement_summary(user_id)
    return ReimbursementSummary(**summary)
