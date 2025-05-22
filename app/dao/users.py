from fastapi import APIRouter
from psycopg2.extras import RealDictRow

from app.db.settings import connection_async
from app.schemas.users import UserCreate
from app.utils.schemas import get_ulid_to_string
from pydantic_extra_types.ulid import ULID

router = APIRouter()


async def select_all_users() -> list[RealDictRow]:
    """
    Affiche les utilisateurs stockés dans la BDD.
    """
    async with connection_async() as conn:
        async with conn.cursor() as cur:
            sql = "SELECT * FROM users"
            await cur.execute(sql)
            return await cur.fetchall()


async def select_user_by_id(user_id: str) -> RealDictRow:
    """
    Affiche un utilisateur stocké dans la BDD.
    """
    async with connection_async() as conn:
        async with conn.cursor() as cur:
            sql = "SELECT * FROM users WHERE id = %s"
            await cur.execute(sql, (user_id,))
            return await cur.fetchone()


async def select_user_by_email(email: str) -> RealDictRow:
    """
    Affiche un utilisateur stocké dans la BDD.
    """
    async with connection_async() as conn:
        async with conn.cursor() as cur:
            sql = "SELECT * FROM users WHERE email = %(email)s"
            await cur.execute(sql, {"email": email})
            return await cur.fetchone()


async def select_users_by_group(group_id: ULID) -> list[RealDictRow]:
    """
    Affiche tout les utilisateurs d'un groupe stockés dans la BDD.
    """
    async with connection_async() as conn:
        async with conn.cursor() as cur:
            sql = "SELECT * FROM users_groups WHERE group_id = %(group_id)s"
            await cur.execute(sql, {"group_id": get_ulid_to_string(group_id)})
            return await cur.fetchall()


async def insert_user(user: UserCreate) -> RealDictRow:
    """
    Crée un utilisateur dans la BDD.
    """
    async with connection_async() as conn:
        async with conn.cursor() as cur:
            sql = """
                  INSERT INTO users (firstname, lastname, password, year_of_birth, address, phone_number, email)
                  VALUES (%(firstname)s,
                          %(lastname)s,
                          %(password)s,
                          %(year_of_birth)s,
                          %(address)s,
                          %(phone_number)s,
                          %(email)s) RETURNING *
                  """
            params = {
                "firstname": user.firstname,
                "lastname": user.lastname,
                "password": user.password.get_secret_value(),
                "year_of_birth": user.year_of_birth,
                "address": user.address,
                "phone_number": user.phone_number,
                "email": user.email,
            }
            await cur.execute(sql, params)
            return await cur.fetchone()


async def update_user(user_id: str, user: UserCreate) -> RealDictRow:
    """
    Modifie un utilisateur dans la BDD.
    """
    async with connection_async() as conn:
        async with conn.cursor() as cur:
            sql = """
                  UPDATE users
                  SET firstname     = %(firstname)s,
                      lastname      = %(lastname)s,
                      password      = %(password)s,
                      year_of_birth = %(year_of_birth)s,
                      address       = %(address)s,
                      phone_number  = %(phone_number)s,
                      email         = %(email)s
                  WHERE id = %(id)s RETURNING *
                  """
            params = {
                "firstname": user.firstname,
                "lastname": user.lastname,
                "password": user.password.get_secret_value(),
                "date_of_birth": user.date_of_birth,
                "address": user.address,
                "phone_number": user.phone_number,
                "email": user.email,
                "id": user_id,
            }
            await cur.execute(sql, params)
            return await cur.fetchone()


async def soft_delete_user(user_id: str):
    """
    Supprime un utilisateur dans la BDD.
    """
    async with connection_async() as conn:
        async with conn.cursor() as cur:
            sql = "UPDATE users SET deleted_at = NOW() WHERE id = %s"
            await cur.execute(sql, (user_id,))
