from fastapi import APIRouter
from psycopg2.extras import RealDictRow

from app.db.settings import connection_async
from app.schemas.users import UsersCreate

router = APIRouter()


async def select_all_users() -> list[RealDictRow]:
    """
    Affiche les utilisateurs stockés dans la BDD.
    """
    async with connection_async() as conn:
        async with conn.cursor() as cur:
            sql = "SELECT * FROM users"
            await cur.execute(sql)
            result = await cur.fetchall()
    return result


async def select_user_by_id(user_id: str) -> RealDictRow:
    """
    Affiche un utilisateur stocké dans la BDD.
    """
    async with connection_async() as conn:
        async with conn.cursor() as cur:
            sql = "SELECT * FROM users WHERE id = %s"
            await cur.execute(sql, (user_id,))
            result = await cur.fetchone()
    return result


async def insert_user(user: UsersCreate) -> RealDictRow:
    """
    Crée un utilisateur dans la BDD.
    """
    async with connection_async() as conn:
        async with conn.cursor() as cur:
            sql = """
                  INSERT INTO users (firstname, lastname, password, age, address, phone_number, email)
                  VALUES (%(firstname)s,
                          %(lastname)s,
                          %(password)s,
                          %(date_of_birth)s,
                          %(address)s,
                          %(phone_number)s,
                          %(email)s) RETURNING *
                  """
            params = {
                "firstname": user.firstname,
                "lastname": user.lastname,
                "password": user.password.get_secret_value(),
                "date_of_birth": user.date_of_birth,
                "address": user.address,
                "phone_number": user.phone_number,
                "email": user.email,
            }
            await cur.execute(sql, params)
            result = await cur.fetchone()
    return result


async def update_user(user_id: str, user: UsersCreate) -> RealDictRow:
    """
    Modifie un utilisateur dans la BDD.
    """
    async with connection_async() as conn:
        async with conn.cursor() as cur:
            sql = """
                  UPDATE users
                  SET firstname = %(firstname)s,
                      lastname = %(lastname)s,
                      password = %(password)s,
                      date_of_birth = %(date_of_birth)s,
                      address = %(address)s,
                      phone_number = %(phone_number)s,
                      email = %(email)s
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