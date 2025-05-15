from app.dao.spendings import select_spendings_by_group, select_spending_by_id, insert_spending, update_spending_by_id
from app.models.spendings import format_spendings_from_raw, format_spending_from_raw
from app.schemas.spendings import Spending, SpendingCreate


async def fetch_spending_by_id(spending_id) -> Spending:
    """
    Affiche une dépense stockée dans la BDD.
    """
    raw_spending = await select_spending_by_id(spending_id)
    spending = format_spending_from_raw(raw_spending)
    return spending


async def fetch_spendings_by_group(group_id: str) -> list[Spending]:
    """
    Affiche les dépenses stockées dans la BDD.
    """
    raw_spendings = await select_spendings_by_group(group_id)
    spendings = format_spendings_from_raw(raw_spendings)
    return spendings


async def create_spending(spending: SpendingCreate) -> Spending:
    """
    Crée une dépense dans la BDD.
    """
    raw_spending = await insert_spending(spending)
    spending = format_spending_from_raw(raw_spending)
    return spending


async def edit_spending(spending_id: str, spending: SpendingCreate) -> Spending:
    """
    Modifie une dépense dans la BDD.
    """
    raw_spending = await update_spending_by_id(spending_id, spending)
    spending = format_spending_from_raw(raw_spending)
    return spending


async def remove_spending(spending_id: int) -> str:
    """
    Supprime une dépense dans la BDD.
    """
    spending = await select_spending_by_id(spending_id)
    if not spending:
        return f"Spending {spending_id} not found"
    return f"Spending {spending_id} deleted"
