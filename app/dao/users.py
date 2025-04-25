from fastapi import APIRouter
from psycopg2.extras import RealDictRow

from app.db.settings import connection_async
from app.schemas.users import UsersCreate

router = APIRouter()

async def get_all_users() -> list[RealDictRow]:
    """
    Affiche les utilisateurs stockés dans la BDD.
    """
    async with connection_async() as conn:
        async with conn.cursor() as cur:
            sql = "SELECT * FROM Users"
            await cur.execute(sql)
            return await cur.fetchall()


async def create_user(user: UsersCreate) -> RealDictRow:
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
                          %(email)s) RETURNING * \
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
            return await cur.fetchone()
