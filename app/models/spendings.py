from pathlib import WindowsPath, Path

from psycopg2.extras import RealDictRow

from app.schemas.spendings import Spending


def format_spending_from_raw(raw_spending: RealDictRow) -> Spending:
    for key in raw_spending:
        if isinstance(raw_spending[key], WindowsPath):
            raw_spending[key] = Path(raw_spending[key])
    return Spending(**raw_spending)


def format_spendings_from_raw(raw_spendings: list[RealDictRow]) -> list[Spending]:
    """
    Formate les dépenses bruts en objets Spending.
    """
    return [format_spending_from_raw(raw_spending) for raw_spending in raw_spendings]
