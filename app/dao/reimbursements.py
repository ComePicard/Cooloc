from psycopg2.extras import RealDictRow

from app.db.settings import connection_async
from app.dao.spendings import select_spending_by_id
from app.dao.users_groups import get_users_in_group
from app.schemas.reimbursements import SpendingReimbursementCreate
from app.utils.schemas import get_ulid_to_string
from pydantic_extra_types.ulid import ULID


async def select_reimbursements_by_spending(spending_id: str) -> list[RealDictRow]:
    """
    Affiche les remboursements pour une dépense.
    """
    async with connection_async() as conn:
        async with conn.cursor() as cur:
            sql = "SELECT * FROM spending_reimbursements WHERE spending_id = %(spending_id)s"
            params = {"spending_id": spending_id}
            await cur.execute(sql, params)
            return await cur.fetchall()


async def select_reimbursements_by_user(user_id: ULID) -> list[RealDictRow]:
    """
    Affiche les remboursements pour un utilisateur.
    """
    async with connection_async() as conn:
        async with conn.cursor() as cur:
            sql = "SELECT * FROM spending_reimbursements WHERE user_id = %(user_id)s"
            params = {"user_id": get_ulid_to_string(user_id)}
            await cur.execute(sql, params)
            return await cur.fetchall()


async def insert_reimbursement(spending_id: str, user_id: ULID, reimbursement_amount: float) -> RealDictRow:
    """
    Crée un remboursement dans la BDD avec le montant spécifié.
    """
    async with connection_async() as conn:
        async with conn.cursor() as cur:
            sql = """
                  INSERT INTO spending_reimbursements (spending_id,
                                                       user_id,
                                                       reimbursement_amount,
                                                       reimbursed_at)
                  VALUES (%(spending_id)s,
                          %(user_id)s,
                          %(reimbursement_amount)s,
                          NULL) RETURNING *
                  """
            params = {
                "spending_id": spending_id,
                "user_id": get_ulid_to_string(user_id),
                "reimbursement_amount": reimbursement_amount
            }
            await cur.execute(sql, params)
            return await cur.fetchone()


async def delete_reimbursement(spending_id: str, user_id: str) -> None:
    """
    Supprime un remboursement de la BDD.
    """
    async with connection_async() as conn:
        async with conn.cursor() as cur:
            sql = """
                  DELETE
                  FROM spending_reimbursements
                  WHERE spending_id = %(spending_id)s
                    AND user_id = %(user_id)s
                  """
            params = {
                "spending_id": spending_id,
                "user_id": user_id
            }
            await cur.execute(sql, params)

            sql_update = """
                         UPDATE Spendings
                         SET is_reimbursed = FALSE
                         WHERE id = %(spending_id)s
                         """
            await cur.execute(sql_update, {"spending_id": spending_id})


async def update_reimbursement_paid_at(spending_id: str, user_id: str, paid_at) -> None:
    """
    Met à jour la date de paiement d'un remboursement.
    """
    async with connection_async() as conn:
        async with conn.cursor() as cur:
            sql = """
                  UPDATE spending_reimbursements
                  SET reimbursed_at = %(reimbursed_at)s
                  WHERE spending_id = %(spending_id)s AND user_id = %(user_id)s
                  """
            params = {
                "spending_id": spending_id,
                "user_id": user_id,
                "reimbursed_at": paid_at
            }
            await cur.execute(sql, params)

        async with conn.cursor() as cur:
            sql = "SELECT * FROM spending_reimbursements WHERE spending_id = %(spending_id)s"
            params = {"spending_id": spending_id}
            await cur.execute(sql, params)
            all_reimboursements = await cur.fetchall()
            full_reimbursements = True
            for reimbursement in all_reimboursements:
                if reimbursement["reimbursed_at"] is None:
                    full_reimbursements = False

        if  full_reimbursements:
            async with conn.cursor() as cur:
                sql_update = """
                             UPDATE spendings
                             SET is_reimbursed = TRUE
                             WHERE id = %(spending_id)s \
                             """
                await cur.execute(sql_update, {"spending_id": spending_id})


async def select_unpaid_reimbursements_by_user(user_id: ULID) -> list[RealDictRow]:
    """
    Récupère tous les remboursements non payés pour un utilisateur.
    """
    async with connection_async() as conn:
        async with conn.cursor() as cur:
            sql = """
                  SELECT * FROM spending_reimbursements
                  WHERE user_id = %(user_id)s AND reimbursed_at IS NULL
                  """
            params = {"user_id": get_ulid_to_string(user_id)}
            await cur.execute(sql, params)
            return await cur.fetchall()


async def select_total_reimbursements_owed_by_user(user_id: ULID) -> float:
    """
    Calcule le montant total des remboursements dus par un utilisateur.
    """
    async with connection_async() as conn:
        async with conn.cursor() as cur:
            sql = """
                  SELECT COALESCE(SUM(reimbursement_amount), 0) as total_owed
                  FROM spending_reimbursements
                  WHERE user_id = %(user_id)s
                  """
            params = {"user_id": get_ulid_to_string(user_id)}
            await cur.execute(sql, params)
            result = await cur.fetchone()
            return float(result["total_owed"]) if result else 0.0


async def select_total_reimbursements_owed_to_user(user_id: ULID) -> float:
    """
    Calcule le montant total des remboursements dus à un utilisateur.
    """
    async with connection_async() as conn:
        async with conn.cursor() as cur:
            sql = """
                  SELECT COALESCE(SUM(sr.reimbursement_amount), 0) as total_owed
                  FROM spending_reimbursements sr
                  JOIN spendings s ON sr.spending_id = s.id
                  WHERE s.owner_id = %(user_id)s
                  """
            params = {"user_id": get_ulid_to_string(user_id)}
            await cur.execute(sql, params)
            result = await cur.fetchone()
            return float(result["total_owed"]) if result else 0.0
