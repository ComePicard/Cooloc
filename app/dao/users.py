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
            sql = "SELECT * FROM Users"
            await cur.execute(sql)
            result = await cur.fetchall()
    return result


async def select_user_by_id(user_id: str) -> RealDictRow:
    """
    Affiche un utilisateur stocké dans la BDD.
    """
    async with connection_async() as conn:
        async with conn.cursor() as cur:
            sql = "SELECT * FROM Users WHERE id = %s"
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
                  INSERT INTO Users (firstname, lastname, password, age, address, phone_number, email)
                  VALUES (%(firstname)s,
                          %(lastname)s,
                          %(password)s,
                          %(age)s,
                          %(address)s,
                          %(phone_number)s,
                          %(email)s) RETURNING *
                  """
            params = {
                "firstname": user.firstname,
                "lastname": user.lastname,
                "password": user.password.get_secret_value(),
                "age": user.age,
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
                  UPDATE Users
                  SET firstname = %(firstname)s,
                      lastname = %(lastname)s,
                      password = %(password)s,
                      age = %(age)s,
                      address = %(address)s,
                      phone_number = %(phone_number)s,
                      email = %(email)s
                  WHERE id = %s RETURNING *
                  """
            params = {
                "firstname": user.firstname,
                "lastname": user.lastname,
                "password": user.password.get_secret_value(),
                "age": user.age,
                "address": user.address,
                "phone_number": user.phone_number,
                "email": user.email,
            }
            await cur.execute(sql, (*params.values(), user_id))
            result = await cur.fetchone()
    return result


async def delete_user(user_id: str):
    """
    Supprime un utilisateur dans la BDD.
    """
    async with connection_async() as conn:
        async with conn.cursor() as cur:
            sql = "DELETE FROM Users WHERE id = %s"
            await cur.execute(sql, (user_id,))