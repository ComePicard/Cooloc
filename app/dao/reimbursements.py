from psycopg2.extras import RealDictRow

from app.db.settings import connection_async
from app.schemas.reimbursements import SpendingReimbursementCreate
from app.utils.schemas import get_ulid_to_string

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


async def select_reimbursements_by_user(user_id: str) -> list[RealDictRow]:
    """
    Affiche les remboursements pour un utilisateur.
    """
    async with connection_async() as conn:
        async with conn.cursor() as cur:
            sql = "SELECT * FROM spending_reimbursements WHERE user_id = %(user_id)s"
            params = {"user_id": user_id}
            await cur.execute(sql, params)
            return await cur.fetchall()


async def insert_reimbursement(reimbursement: SpendingReimbursementCreate) -> RealDictRow:
    """
    Crée un remboursement dans la BDD.
    """
    async with connection_async() as conn:
        async with conn.cursor() as cur:
            # First, update the spending to mark it as reimbursed
            sql_update_spending = """
                                  UPDATE Spendings
                                  SET is_reimbursed = TRUE
                                  WHERE id = %(spending_id)s RETURNING *
                                  """
            params_update = {
                "spending_id": get_ulid_to_string(reimbursement.spending_id)
            }
            await cur.execute(sql_update_spending, params_update)

            # Then, insert the reimbursement record
            sql = """
                  INSERT INTO spending_reimbursements (spending_id,
                                                       user_id)
                  VALUES (%(spending_id)s,
                          %(user_id)s) RETURNING *
                  """
            params = {
                "spending_id": get_ulid_to_string(reimbursement.spending_id),
                "user_id": get_ulid_to_string(reimbursement.user_id)
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

            # Check if there are any remaining reimbursements for this spending
            sql_check = """
                        SELECT COUNT(*)
                        FROM spending_reimbursements
                        WHERE spending_id = %(spending_id)s
                        """
            await cur.execute(sql_check, {"spending_id": spending_id})
            count = await cur.fetchone()

            # If no reimbursements remain, update the spending to mark it as not reimbursed
            if count and count[0] == 0:
                sql_update = """
                             UPDATE Spendings
                             SET is_reimbursed = FALSE
                             WHERE id = %(spending_id)s
                             """
                await cur.execute(sql_update, {"spending_id": spending_id})
