from psycopg2.extras import RealDictRow

from app.dao.spendings import select_spendings_by_group, select_spending_by_id, select_spendings_by_user, \
    insert_spending
from app.models.spendings import format_spendings_from_raw, format_spending_from_raw
from app.schemas.spendings import Spending, SpendingCreate


async def fetch_spending_by_id(spending_id) -> Spending:
    """
    Affiche un spending stocké dans la BDD.
    """
    raw_spending = await select_spending_by_id(spending_id)
    spending = format_spending_from_raw(raw_spending)
    return spending


async def fetch_spendings_by_group(group_id: str) -> list[Spending]:
    """
    Affiche les spendings stockés dans la BDD.
    """
    raw_spendings = await select_spendings_by_group(group_id)
    spendings = format_spendings_from_raw(raw_spendings)
    return spendings


async def fetch_spendings_by_user(user: str) -> list[Spending]:
    """
    Affiche les spendings stockés dans la BDD.
    """
    raw_spendings = await select_spendings_by_user(user)
    spendings = format_spendings_from_raw(raw_spendings)
    return spendings


async def create_spending(spending: SpendingCreate) -> Spending:
    """
    Crée un spending dans la BDD.
    """
    raw_spending = await insert_spending(spending)
    spending = format_spending_from_raw(raw_spending)
    return spending

async def edit_spending(spending_id: int, spending: SpendingCreate) -> Spending:
    """
    Modifie un spending dans la BDD.
    """
    raw_spending = await insert_spending(spending)
    spending = format_spending_from_raw(raw_spending)
    return spending


async def remove_spending(spending_id: int) -> str:
    """
    Supprime un spending dans la BDD.
    """
    spending = await select_spending_by_id(spending_id)
    if not spending:
        return f"Document {spending_id} not found"
    return f"Document {spending_id} deleted"