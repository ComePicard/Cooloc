from psycopg2.extras import RealDictRow

from app.db.settings import connection_async
from app.schemas.spendings import SpendingsCreate
from app.utils.schemas import get_ulid_to_string


async def select_spending_by_id(spending_id: int) -> RealDictRow:
    """
    Affiche un spending stocké dans la BDD.
    """
    async with connection_async() as conn:
        async with conn.cursor() as cur:
            sql = "SELECT * FROM spendings WHERE id = %s"
            params = {"spending_id": spending_id}
            await cur.execute(sql, params)
            return await cur.fetchone()


async def select_spendings_by_group(group_id: str) -> RealDictRow:
    """
    Affiche les spendings stockés dans la BDD.
    """
    async with connection_async() as conn:
        async with conn.cursor() as cur:
            sql = "SELECT * FROM spendings WHERE group_id = %s"
            params = {"group_id": group_id}
            await cur.execute(sql, params)
            return await cur.fetchall()


async def select_spendings_by_user(user: str) -> RealDictRow:
    """
    Affiche les spendings stockés dans la BDD.
    """
    async with connection_async() as conn:
        async with conn.cursor() as cur:
            sql = "SELECT * FROM spendings WHERE group_id = %s"
            params = {"user_id": user}
            await cur.execute(sql, params)
            return await cur.fetchall()


async def insert_spending(spending: SpendingsCreate) -> RealDictRow:
    """
    Crée un spending dans la BDD.
    """
    async with connection_async() as conn:
        async with conn.cursor() as cur:
            sql = """
                INSERT INTO spendings (
                    name,
                    description,
                    amount,
                    currency,
                    owner_id,
                    group_id
                )
                VALUES (
                    %(name)s,
                    %(description)s,
                    %(amount)s,
                    %(currency)s,
                    %(owner_id)s,
                    %(group_id)s
               ) RETURNING *
            """
            params = {
                "name": spending.name,
                "description": spending.description,
                "amount": spending.amount,
                "currency": spending.currency,
                "owner_id": get_ulid_to_string(spending.owner_id),
                "group_id": get_ulid_to_string(spending.group_id),
            }
            await cur.execute(sql, params)
            return await cur.fetchone()


async def update_spending_by_id(spending_id: str, spending: SpendingsCreate) -> RealDictRow:
    """
    Met à jour un spending dans la BDD.
    """
    async with connection_async() as conn:
        async with conn.cursor() as cur:
            sql = """
                UPDATE spendings
                SET 
                    name = %(name)s,
                    description = %(description)s,
                    amount = %(amount)s,
                    currency = %(currency)s,
                    owner_id = %(owner_id)s,
                    group_id = %(group_id)s
                WHERE id = %(id)s
                RETURNING *
            """
            params = {
                "name": spending.name,
                "description": spending.description,
                "amount": spending.amount,
                "currency": spending.currency,
                "owner_id": get_ulid_to_string(spending.owner_id),
                "group_id": get_ulid_to_string(spending.group_id),
                "id": spending_id,
            }
            await cur.execute(sql, params)
            return await cur.fetchone()


async def soft_delete_spending_by_id(spending_id: int) -> None:
    """
    Supprime un spending de la BDD.
    """
    async with connection_async() as conn:
        async with conn.cursor() as cur:
            sql = "UPDATE deleted_at=NOW() FROM spendings WHERE id = %(id)s"
            params = {"id": spending_id}
            await cur.execute(sql, params)