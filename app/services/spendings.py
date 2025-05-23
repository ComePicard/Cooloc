from app.dao.reimbursements import insert_reimbursement
from app.dao.spendings import select_spendings_by_group, select_spending_by_id, insert_spending, update_spending_by_id, \
    select_spendings_by_user
from app.dao.users import select_users_by_group
from app.models.reimbursements import format_spending_reimbursement_from_raw
from app.models.spendings import format_spendings_from_raw, format_spending_from_raw
from app.schemas.auth import TokenData
from app.schemas.reimbursements import SpendingReimbursementCreate
from app.schemas.spendings import Spending, SpendingCreate
from app.services.users import fetch_user_by_email


async def fetch_spending_by_id(spending_id) -> Spending:
    """
    Affiche une dépense stockée dans la BDD.
    """
    raw_spending = await select_spending_by_id(spending_id)
    spending = format_spending_from_raw(raw_spending)
    return spending


async def fetch_spendings_by_user_id(current_user: TokenData) -> list[Spending]:
    """
    Affiche la/les dépense(s) de l'utilisateur connecté.
    """
    owner = await fetch_user_by_email(current_user.email)
    raw_spendings = await select_spendings_by_user(owner.id)
    spendings = format_spendings_from_raw(raw_spendings)
    return spendings


async def fetch_spendings_by_group(group_id: str) -> list[Spending]:
    """
    Affiche les dépenses stockées dans la BDD.
    """
    raw_spendings = await select_spendings_by_group(group_id)
    spendings = format_spendings_from_raw(raw_spendings)
    return spendings


async def create_spending(spending: SpendingCreate, current_user: TokenData) -> Spending:
    """
    Crée une dépense dans la BDD et génère automatiquement des remboursements
    pour tous les utilisateurs du groupe (sauf le propriétaire).
    Le montant du remboursement est calculé en divisant le montant de la dépense
    par le nombre de personnes dans le groupe (excluant le propriétaire).
    """
    owner = await fetch_user_by_email(current_user.email)
    raw_spending = await insert_spending(spending, owner.id)
    spending = format_spending_from_raw(raw_spending)
    group_users_raw = await select_users_by_group(spending.group_id)
    total_users_count = len(group_users_raw)

    if total_users_count > 0:
        per_person_amount = float(spending.amount) / total_users_count
        reimbursement_amount = per_person_amount
    else:
        reimbursement_amount = 0.0

    for group_user in group_users_raw:
        if group_user["user_id"] != str(owner.id):
            await insert_reimbursement(str(spending.id), group_user["user_id"], reimbursement_amount)

    return spending


async def edit_spending(spending_id: str, spending: SpendingCreate) -> Spending:
    """
    Modifie une dépense dans la BDD.
    """
    raw_spending = await update_spending_by_id(spending_id, spending)
    spending = format_spending_from_raw(raw_spending)
    return spending
