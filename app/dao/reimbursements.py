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
            params = {"user_id": user_id}
            await cur.execute(sql, params)
            return await cur.fetchall()


async def insert_reimbursement(reimbursement: SpendingReimbursementCreate, user_id: ULID) -> RealDictRow:
    """
    Crée un remboursement dans la BDD.
    """
    async with connection_async() as conn:
        async with conn.cursor() as cur:
            # First, insert the reimbursement record
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
            reimbursement_record = await cur.fetchone()

            # Get the spending to check its group_id
            spending_id_str = get_ulid_to_string(reimbursement.spending_id)
            spending = await select_spending_by_id(spending_id_str)

            if not spending:
                return reimbursement_record

            # Get all users in the group
            group_users = await get_users_in_group(spending["group_id"])

            if not group_users:
                return reimbursement_record

            # Get all reimbursements for this spending
            sql_reimbursements = """
                SELECT user_id FROM spending_reimbursements
                WHERE spending_id = %(spending_id)s
            """
            await cur.execute(sql_reimbursements, {"spending_id": spending_id_str})
            reimbursements = await cur.fetchall()

            # Extract user IDs who have reimbursed
            reimbursed_user_ids = {r["user_id"] for r in reimbursements}

            # Check if all users (except the owner) have reimbursed
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
                sql_update_spending = """
                    UPDATE Spendings
                    SET is_reimbursed = TRUE
                    WHERE id = %(spending_id)s
                """
                await cur.execute(sql_update_spending, {"spending_id": spending_id_str})

            return reimbursement_record


async def delete_reimbursement(spending_id: str, user_id: str) -> None:
    """
    Supprime un remboursement de la BDD.
    """
    async with connection_async() as conn:
        async with conn.cursor() as cur:
            # First, delete the reimbursement
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

            # Always mark the spending as not reimbursed when a reimbursement is deleted
            # since at least one user hasn't reimbursed it
            sql_update = """
                         UPDATE Spendings
                         SET is_reimbursed = FALSE
                         WHERE id = %(spending_id)s
                         """
            await cur.execute(sql_update, {"spending_id": spending_id})
