from fastapi import APIRouter
from psycopg2.extras import RealDictRow

from app.db.settings import connection_async
from app.schemas.groups import GroupCreate

router = APIRouter()


async def select_all_groups() -> list[RealDictRow]:
    """
    Affiche les utilisateurs stockés dans la BDD.
    """
    async with connection_async() as conn:
        async with conn.cursor() as cur:
            sql = "SELECT * FROM groups"
            await cur.execute(sql)
            return await cur.fetchall()


async def select_group_by_id(group_id: str) -> RealDictRow:
    """
    Affiche un utilisateur stocké dans la BDD.
    """
    async with connection_async() as conn:
        async with conn.cursor() as cur:
            sql = "SELECT * FROM groups WHERE id = %s"
            await cur.execute(sql, (group_id,))
            return await cur.fetchone()


async def insert_group(group: GroupCreate) -> RealDictRow:
    """
    Crée un utilisateur dans la BDD.
    """
    async with connection_async() as conn:
        async with conn.cursor() as cur:
            sql = """
                  INSERT INTO groups (firstname, id)
                  VALUES (%(firstname)s,
                          %(id)s) RETURNING *
                  """
            params = {
                "firstname": group.firstname,
                "id": group.id,
            }
            await cur.execute(sql, params)
            return await cur.fetchone()


async def update_group(group_id: str, group: GroupCreate) -> RealDictRow:
    """
    Modifie un utilisateur dans la BDD.
    """
    async with connection_async() as conn:
        async with conn.cursor() as cur:
            sql = """
                  UPDATE groups
                  SET firstname = %(firstname)s,
                  WHERE id = %(id)s RETURNING *
                  """
            params = {
                "firstname": group.firstname,
                "id": group_id,
            }
            await cur.execute(sql, params)
            return await cur.fetchone()


async def soft_delete_group(group_id: str):
    """
    Supprime un utilisateur dans la BDD.
    """
    async with connection_async() as conn:
        async with conn.cursor() as cur:
            sql = "UPDATE groups SET deleted_at = NOW() WHERE id = %s"
            await cur.execute(sql, (group_id,))