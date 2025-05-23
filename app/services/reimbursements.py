from pydantic_extra_types.ulid import ULID

from app.dao.reimbursements import (
    select_reimbursements_by_spending, select_reimbursements_by_user, insert_reimbursement, delete_reimbursement,
    select_total_reimbursements_owed_by_user, select_total_reimbursements_owed_to_user
)
from app.models.reimbursements import (
    format_spending_reimbursement_from_raw, format_spending_reimbursements_from_raw
)
from app.schemas.auth import TokenData
from app.schemas.reimbursements import SpendingReimbursement, SpendingReimbursementCreate
from app.services.users import fetch_user_by_email, fetch_user_by_id
from app.utils.schemas import get_ulid_to_string


async def fetch_reimbursements_by_spending(spending_id: str) -> list[SpendingReimbursement]:
    """
    Affiche les remboursements pour une dépense.
    """
    raw_reimbursements = await select_reimbursements_by_spending(spending_id)
    reimbursements = format_spending_reimbursements_from_raw(raw_reimbursements)
    return reimbursements


async def fetch_reimbursements_by_user(current_user: TokenData) -> list[SpendingReimbursement]:
    """
    Affiche les remboursements pour un utilisateur.
    """
    owner = await fetch_user_by_email(current_user.email)
    raw_reimbursements = await select_reimbursements_by_user(owner.id)
    reimbursements = format_spending_reimbursements_from_raw(raw_reimbursements)
    return reimbursements


async def create_reimbursement(reimbursement: SpendingReimbursementCreate,
                               current_user: TokenData) -> list[SpendingReimbursement]:
    """
    Crée un remboursement pour chaque utilisateur du groupe (hors owner).
    """
    from app.dao.spendings import select_spending_by_id
    from app.dao.users_groups import get_users_in_group

    owner = await fetch_user_by_email(current_user.email)
    spending_id_str = get_ulid_to_string(reimbursement.spending_id)
    spending = await select_spending_by_id(spending_id_str)

    if not spending:
        raise ValueError(f"Spending {spending_id_str} not found")

    group_users = await get_users_in_group(spending["group_id"])
    if not group_users:
        raise ValueError(f"No users found in group {spending['group_id']}")

    total_users_count = len(group_users)
    if total_users_count > 1:
        per_person_amount = float(spending["amount"]) / total_users_count
    else:
        per_person_amount = 0.0

    from app.dao.reimbursements import insert_reimbursement

    reimbursements = []
    for user in group_users:
        if user["id"] == spending["owner_id"]:
            continue
        raw_reimbursement = await insert_reimbursement(
            spending_id_str,
            user["id"],
            per_person_amount
        )
        formatted = format_spending_reimbursement_from_raw(raw_reimbursement)
        reimbursements.append(formatted)

    return reimbursements


async def remove_reimbursement(spending_id: str, user_id: str) -> str:
    """
    Supprime un remboursement de la BDD.
    """
    await delete_reimbursement(spending_id, user_id)
    return f"Reimbursement for spending {spending_id} and user {user_id} deleted"


async def mark_reimbursement_as_paid(spending_id: str, user_id: str, paid_at) -> None:
    """
    Marque un remboursement comme payé (ajoute une date de paiement).
    """
    from app.dao.reimbursements import update_reimbursement_paid_at
    await update_reimbursement_paid_at(spending_id, user_id, paid_at)


async def fetch_unpaid_reimbursements_by_user(current_user: TokenData) -> list[SpendingReimbursement]:
    """
    Récupère tous les remboursements non payés pour l'utilisateur courant.
    """
    from app.dao.reimbursements import select_unpaid_reimbursements_by_user
    owner = await fetch_user_by_email(current_user.email)
    raws = await select_unpaid_reimbursements_by_user(owner.id)
    return format_spending_reimbursements_from_raw(raws)


async def fetch_total_reimbursements_owed_by_user(user_id: str) -> float:
    """
    Calcule le montant total des remboursements dus par un utilisateur.
    """
    owner = await fetch_user_by_id(user_id)
    return await select_total_reimbursements_owed_by_user(owner.id)


async def fetch_total_reimbursements_owed_to_user(user_id: str) -> float:
    """
    Calcule le montant total des remboursements dus à un utilisateur.
    """
    owner = await fetch_user_by_id(user_id)
    return await select_total_reimbursements_owed_to_user(owner.id)


async def fetch_reimbursement_summary(current_user: TokenData) -> dict:
    """
    Calcule le résumé des remboursements pour un utilisateur.
    """
    owner = await fetch_user_by_email(current_user.email)
    total_owed_by = await fetch_total_reimbursements_owed_by_user(str(owner.id))
    total_owed_to = await fetch_total_reimbursements_owed_to_user(str(owner.id))
    balance = total_owed_to - total_owed_by

    return {
        "total_owed_by": total_owed_by,
        "total_owed_to": total_owed_to,
        "balance": balance
    }
