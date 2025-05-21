from psycopg2.extras import RealDictRow
from app.schemas.reimbursements import SpendingReimbursement


def format_spending_reimbursement_from_raw(raw_reimbursement: RealDictRow) -> SpendingReimbursement:
    """
    Formate un remboursement brut en objet SpendingReimbursement.
    """
    return SpendingReimbursement(**raw_reimbursement)


def format_spending_reimbursements_from_raw(raw_reimbursements: list[RealDictRow]) -> list[SpendingReimbursement]:
    """
    Formate les remboursements bruts en objets SpendingReimbursement.
    """
    return [format_spending_reimbursement_from_raw(raw_reimbursement) for raw_reimbursement in raw_reimbursements]
