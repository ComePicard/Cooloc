from psycopg2.extras import RealDictRow

from app.db.settings import connection_async
from pydantic_extra_types.ulid import ULID

from app.utils.schemas import get_ulid_to_string


async def add_user_to_group(user_id: ULID, group_id: str) -> RealDictRow:
    """
    Ajoute un utilisateur à un groupe.
    """
    async with connection_async() as conn:
        async with conn.cursor() as cur:
            # Check if the user is already in the group
            check_sql = """
                SELECT 1 FROM users_groups 
                WHERE user_id = %(user_id)s AND group_id = %(group_id)s
            """
            params = {
                "user_id": get_ulid_to_string(user_id),
                "group_id": group_id
            }
            await cur.execute(check_sql, params)
            exists = await cur.fetchone()
            
            # If the user is already in the group, return the existing relationship
            if exists:
                return exists
            
            # Otherwise, add the user to the group
            sql = """
                INSERT INTO users_groups (user_id, group_id)
                VALUES (%(user_id)s, %(group_id)s)
                RETURNING *
            """
            await cur.execute(sql, params)
            return await cur.fetchone()


async def remove_user_from_group(user_id: str, group_id: str) -> None:
    """
    Retire un utilisateur d'un groupe.
    """
    async with connection_async() as conn:
        async with conn.cursor() as cur:
            sql = """
                DELETE FROM users_groups
                WHERE user_id = %(user_id)s AND group_id = %(group_id)s
            """
            params = {
                "user_id": user_id,
                "group_id": group_id
            }
            await cur.execute(sql, params)


async def is_user_in_group(user_id: str, group_id: str) -> bool:
    """
    Vérifie si un utilisateur est membre d'un groupe.
    """
    async with connection_async() as conn:
        async with conn.cursor() as cur:
            sql = """
                SELECT 1 FROM users_groups
                WHERE user_id = %(user_id)s AND group_id = %(group_id)s
            """
            params = {
                "user_id": user_id,
                "group_id": group_id
            }
            await cur.execute(sql, params)
            result = await cur.fetchone()
            return result is not None


async def get_users_in_group(group_id: str) -> list[RealDictRow]:
    """
    Récupère tous les utilisateurs membres d'un groupe.
    """
    async with connection_async() as conn:
        async with conn.cursor() as cur:
            sql = """
                SELECT u.* FROM users u
                JOIN users_groups ug ON u.id = ug.user_id
                WHERE ug.group_id = %(group_id)s
            """
            params = {
                "group_id": group_id
            }
            await cur.execute(sql, params)
            return await cur.fetchall()


async def get_groups_for_user(user_id: ULID) -> list[RealDictRow]:
    """
    Récupère tous les groupes dont un utilisateur est membre.
    """
    async with connection_async() as conn:
        async with conn.cursor() as cur:
            sql = """
                SELECT g.* FROM groups g
                JOIN users_groups ug ON g.id = ug.group_id
                WHERE ug.user_id = %(user_id)s
            """
            params = {
                "user_id": get_ulid_to_string(user_id)
            }
            await cur.execute(sql, params)
            return await cur.fetchall()