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
from app.services.users import fetch_user_by_email
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
                               current_user: TokenData) -> SpendingReimbursement:
    """
    Crée un remboursement dans la BDD.
    Le montant du remboursement est calculé en divisant le montant de la dépense
    par le nombre total de personnes dans le groupe.
    """
    from app.dao.spendings import select_spending_by_id
    from app.dao.users_groups import get_users_in_group

    owner = await fetch_user_by_email(current_user.email)

    # Get the spending to calculate the reimbursement amount
    spending_id_str = get_ulid_to_string(reimbursement.spending_id)
    spending = await select_spending_by_id(spending_id_str)

    if not spending:
        raise ValueError(f"Spending {spending_id_str} not found")

    # Get all users in the group
    group_users = await get_users_in_group(spending["group_id"])

    if not group_users:
        raise ValueError(f"No users found in group {spending['group_id']}")

    # Count total users in the group
    total_users_count = len(group_users)

    # Calculate reimbursement amount
    # Each person pays their part (total amount / number of people in the group)
    if total_users_count > 0:
        # Each person's share is the total amount divided by the number of people
        per_person_amount = float(spending["amount"]) / total_users_count
        # The reimbursement amount is each person's share
        reimbursement_amount = per_person_amount
    else:
        reimbursement_amount = 0.0

    # Insert the reimbursement record with the calculated amount
    raw_reimbursement = await insert_reimbursement(
        spending_id_str, 
        owner.id, 
        reimbursement_amount
    )

    # Check if all users (except the owner) have reimbursed
    reimbursements = await select_reimbursements_by_spending(spending_id_str)
    reimbursed_user_ids = {r["user_id"] for r in reimbursements}

    all_reimbursed = True
    for user in group_users:
        # Skip the owner of the spending
        if user["id"] == spending["owner_id"]:
            continue

        # If a user hasn't reimbursed, mark as not all reimbursed
        if user["id"] not in reimbursed_user_ids:
            all_reimbursed = False
            break

    # If all users have reimbursed, update the spending
    if all_reimbursed:
        from app.dao.spendings import update_spending_by_id
        from app.schemas.spendings import SpendingCreate

        # Create a SpendingCreate object with the updated is_reimbursed value
        updated_spending = SpendingCreate(
            name=spending["name"],
            description=spending["description"],
            amount=spending["amount"],
            currency=spending["currency"],
            is_reimbursed=True,
            owner_id=ULID.from_str(spending["owner_id"]),
            group_id=ULID.from_str(spending["group_id"])
        )

        await update_spending_by_id(spending_id_str, updated_spending)

    formatted_reimbursement = format_spending_reimbursement_from_raw(raw_reimbursement)
    return formatted_reimbursement


async def remove_reimbursement(spending_id: str, user_id: str) -> str:
    """
    Supprime un remboursement de la BDD.
    """
    await delete_reimbursement(spending_id, user_id)
    return f"Reimbursement for spending {spending_id} and user {user_id} deleted"


async def fetch_total_reimbursements_owed_by_user(user_id: ULID) -> float:
    """
    Calcule le montant total des remboursements dus par un utilisateur.
    """
    return await select_total_reimbursements_owed_by_user(user_id)


async def fetch_total_reimbursements_owed_to_user(user_id: ULID) -> float:
    """
    Calcule le montant total des remboursements dus à un utilisateur.
    """
    return await select_total_reimbursements_owed_to_user(user_id)


async def fetch_reimbursement_summary(user_id: TokenData) -> dict:
    """
    Calcule le résumé des remboursements pour un utilisateur.
    """
    owner = await fetch_user_by_email(user_id.email)
    total_owed_by = await fetch_total_reimbursements_owed_by_user(owner.id)
    total_owed_to = await fetch_total_reimbursements_owed_to_user(owner.id)
    balance = total_owed_to - total_owed_by

    return {
        "total_owed_by": total_owed_by,
        "total_owed_to": total_owed_to,
        "balance": balance
    }
