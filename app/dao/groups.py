from fastapi import APIRouter
from psycopg2.extras import RealDictRow

from app.db.settings import connection_async
from app.schemas.groups import GroupCreate

router = APIRouter()


async def select_group_by_id(group_id: str) -> RealDictRow:
    """
    Affiche un groupe stocké dans la BDD.
    """
    async with connection_async() as conn:
        async with conn.cursor() as cur:
            sql = "SELECT * FROM groups WHERE id = %s"
            await cur.execute(sql, (group_id,))
            return await cur.fetchone()


async def insert_group(group: GroupCreate) -> RealDictRow:
    """
    Crée un groupe dans la BDD.
    """
    async with connection_async() as conn:
        async with conn.cursor() as cur:
            sql = """
                  INSERT INTO groups (name,
                                      description,
                                      city,
                                      postal_code,
                                      country,
                                      contact_email,
                                      contact_phone,
                                      agency_email,
                                      agency_phone,
                                      starting_at,
                                      ending_at)
                  VALUES (%(name)s,
                          %(description)s,
                          %(city)s,
                          %(postal_code)s,
                          %(country)s,
                          %(contact_email)s,
                          %(contact_phone)s,
                          %(agency_email)s,
                          %(agency_phone)s,
                          %(starting_at)s,
                          %(ending_at)s) RETURNING *
                  """
            params = {
                "name": group.name,
                "description": group.description,
                "city": group.city,
                "postal_code": group.postal_code,
                "country": group.country,
                "contact_email": group.contact_email,
                "contact_phone": group.contact_phone,
                "agency_email": group.agency_email,
                "agency_phone": group.agency_phone,
                "starting_at": group.starting_at,
                "ending_at": group.ending_at
            }
            await cur.execute(sql, params)
            return await cur.fetchone()


async def update_group(group_id: str, group: GroupCreate) -> RealDictRow:
    """
    Modifie un groupe dans la BDD.
    """
    async with connection_async() as conn:
        async with conn.cursor() as cur:
            sql = """
                  UPDATE groups
                  SET name          = %(name)s,
                      description   = %(description)s,
                      city          = %(city)s,
                      postal_code   = %(postal_code)s,
                      country       = %(country)s,
                      contact_email = %(contact_email)s,
                      contact_phone = %(contact_phone)s,
                      agency_email  = %(agency_email)s,
                      agency_phone  = %(agency_phone)s,
                      starting_at   = %(starting_at)s,
                      ending_at     = %(ending_at)s,
                      updated_at    = NOW()
                  WHERE id = %(id)s RETURNING *
                  """
            params = {
                "name": group.name,
                "description": group.description,
                "city": group.city,
                "postal_code": group.postal_code,
                "country": group.country,
                "contact_email": group.contact_email,
                "contact_phone": group.contact_phone,
                "agency_email": group.agency_email,
                "agency_phone": group.agency_phone,
                "starting_at": group.starting_at,
                "ending_at": group.ending_at,
                "id": group_id
            }
            await cur.execute(sql, params)
            return await cur.fetchone()


async def soft_delete_group(group_id: str):
    """
    Supprime un groupe dans la BDD.
    """
    async with connection_async() as conn:
        async with conn.cursor() as cur:
            sql = "UPDATE groups SET deleted_at = NOW() WHERE id = %s"
            await cur.execute(sql, (group_id,))
