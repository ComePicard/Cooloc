from psycopg2.extras import RealDictRow

from app.db.settings import connection_async
from app.schemas.spendings import SpendingCreate
from app.utils.schemas import get_ulid_to_string
from pydantic_extra_types.ulid import ULID


async def select_spending_by_id(spending_id: str) -> RealDictRow:
    """
    Affiche une dépense stockée dans la BDD.
    """
    async with connection_async() as conn:
        async with conn.cursor() as cur:
            sql = "SELECT * FROM Spendings WHERE id = %(id)s"
            params = {"id": spending_id}
            await cur.execute(sql, params)
            return await cur.fetchone()


async def select_spendings_by_group(group_id: str) -> list[RealDictRow]:
    """
    Affiche les dépenses stockées dans la BDD.
    """
    async with connection_async() as conn:
        async with conn.cursor() as cur:
            sql = "SELECT * FROM Spendings WHERE group_id = %(group_id)s"
            params = {"group_id": group_id}
            await cur.execute(sql, params)
            return await cur.fetchall()


async def select_spendings_by_user(owner_id: ULID) -> list[RealDictRow]:
    """
    Affiche les dépenses stockées dans la BDD.
    """
    async with connection_async() as conn:
        async with conn.cursor() as cur:
            sql = "SELECT * FROM Spendings WHERE owner_id = %(owner_id)s"
            params = {"owner_id": get_ulid_to_string(owner_id)}
            await cur.execute(sql, params)
            return await cur.fetchall()


async def insert_spending(spending: SpendingCreate, owner_id: ULID) -> RealDictRow:
    """
    Crée une dépense dans la BDD.
    """
    async with connection_async() as conn:
        async with conn.cursor() as cur:
            sql = """
                  INSERT INTO Spendings (name,
                                         description,
                                         amount,
                                         currency,
                                         is_reimbursed,
                                         owner_id,
                                         group_id)
                  VALUES (%(name)s,
                          %(description)s,
                          %(amount)s,
                          %(currency)s,
                          %(is_reimbursed)s,
                          %(owner_id)s,
                          %(group_id)s) RETURNING * \
                  """
            params = {
                "name": spending.name,
                "description": spending.description,
                "amount": spending.amount,
                "currency": spending.currency,
                "is_reimbursed": spending.is_reimbursed,
                "owner_id": get_ulid_to_string(owner_id),
                "group_id": get_ulid_to_string(spending.group_id),
            }
            await cur.execute(sql, params)
            return await cur.fetchone()


async def update_spending_by_id(spending_id: str, spending: SpendingCreate) -> RealDictRow:
    """
    Met à jour une dépense dans la BDD.
    """
    async with connection_async() as conn:
        async with conn.cursor() as cur:
            sql = """
                  UPDATE Spendings
                  SET name          = %(name)s,
                      description   = %(description)s,
                      amount        = %(amount)s,
                      currency      = %(currency)s,
                      is_reimbursed = %(is_reimbursed)s,
                      owner_id      = %(owner_id)s,
                      group_id      = %(group_id)s
                  WHERE id = %(id)s RETURNING *
                  """
            params = {
                "name": spending.name,
                "description": spending.description,
                "amount": spending.amount,
                "currency": spending.currency,
                "is_reimbursed": spending.is_reimbursed,
                "owner_id": get_ulid_to_string(spending.owner_id),
                "group_id": get_ulid_to_string(spending.group_id),
                "id": spending_id
            }
            await cur.execute(sql, params)
            return await cur.fetchone()
