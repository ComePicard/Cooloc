from pathlib import WindowsPath, Path

from psycopg2.extras import RealDictRow

from app.schemas.spendings import Spendings


def format_spending_from_raw(raw_spending: RealDictRow) -> Spendings:
    return Spendings(**raw_spending)


def format_spendings_from_raw(raw_spendings: list[RealDictRow]) -> list[Spendings]:
    """
    Formate les spendings bruts en objets spendings.
    """
    return [format_spending_from_raw(raw_spending) for raw_spending in raw_spendings]