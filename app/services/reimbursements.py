from app.dao.reimbursements import (
    select_reimbursements_by_spending, select_reimbursements_by_user, insert_reimbursement, delete_reimbursement
)
from app.models.reimbursements import (
    format_spending_reimbursement_from_raw, format_spending_reimbursements_from_raw
)
from app.schemas.reimbursements import SpendingReimbursement, SpendingReimbursementCreate


async def fetch_reimbursements_by_spending(spending_id: str) -> list[SpendingReimbursement]:
    """
    Affiche les remboursements pour une dépense.
    """
    raw_reimbursements = await select_reimbursements_by_spending(spending_id)
    reimbursements = format_spending_reimbursements_from_raw(raw_reimbursements)
    return reimbursements


async def fetch_reimbursements_by_user(user_id: str) -> list[SpendingReimbursement]:
    """
    Affiche les remboursements pour un utilisateur.
    """
    raw_reimbursements = await select_reimbursements_by_user(user_id)
    reimbursements = format_spending_reimbursements_from_raw(raw_reimbursements)
    return reimbursements


async def create_reimbursement(reimbursement: SpendingReimbursementCreate) -> SpendingReimbursement:
    """
    Crée un remboursement dans la BDD.
    """
    raw_reimbursement = await insert_reimbursement(reimbursement)
    reimbursement = format_spending_reimbursement_from_raw(raw_reimbursement)
    return reimbursement


async def remove_reimbursement(spending_id: str, user_id: str) -> str:
    """
    Supprime un remboursement de la BDD.
    """
    await delete_reimbursement(spending_id, user_id)
    return f"Reimbursement for spending {spending_id} and user {user_id} deleted"
