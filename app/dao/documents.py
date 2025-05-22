from psycopg2.extras import RealDictRow

from app.db.settings import connection_async
from app.schemas.documents import DocumentCreate
from app.utils.schemas import get_ulid_to_string


async def select_document_by_id(document_id: str) -> RealDictRow:
    """
    Affiche un document stocké dans la BDD.
    """
    async with connection_async() as conn:
        async with conn.cursor() as cur:
            sql = "SELECT * FROM documents WHERE id = %s"
            await cur.execute(sql, (document_id,))
            return await cur.fetchone()


async def select_documents_by_group(group_id: str) -> list[RealDictRow]:
    """
    Affiche les documents par groupe stockés dans la BDD.
    """
    async with connection_async() as conn:
        async with conn.cursor() as cur:
            sql = "SELECT * FROM documents WHERE group_id = %s"
            await cur.execute(sql, (group_id,))
            return await cur.fetchall()


async def select_documents_by_user(user_id: str) -> list[RealDictRow]:
    """
    Affiche les documents par utilisateur stockés dans la BDD.
    """
    async with connection_async() as conn:
        async with conn.cursor() as cur:
            sql = "SELECT * FROM documents WHERE owner_id = %s"
            await cur.execute(sql, (user_id,))
            return await cur.fetchall()


async def insert_document(document: DocumentCreate) -> RealDictRow:
    """
    Crée un document dans la BDD.
    """
    async with connection_async() as conn:
        async with conn.cursor() as cur:
            sql = """
                  INSERT INTO documents (name,
                                         description,
                                         file_path,
                                         owner_id,
                                         group_id)
                  VALUES (%(name)s,
                          %(description)s,
                          %(file_path)s,
                          %(owner_id)s,
                          %(group_id)s) RETURNING * \
                  """
            params = {
                "name": document.name,
                "description": document.description,
                "file_path": document.file_path.as_posix(),
                "owner_id": get_ulid_to_string(document.owner_id),
                "group_id": get_ulid_to_string(document.group_id),
            }
            await cur.execute(sql, params)
            return await cur.fetchone()


async def update_document_by_id(document_id: str, document: DocumentCreate) -> RealDictRow:
    """
    Met à jour d'un document dans la BDD.
    """
    async with connection_async() as conn:
        async with conn.cursor() as cur:
            sql = """
                  UPDATE documents
                  SET name        = %(name)s,
                      description = %(description)s,
                      file_path   = %(file_path)s,
                      owner_id    = %(owner_id)s,
                      group_id    = %(group_id)s,
                      updated_at  = NOW()
                  WHERE id = %(id)s RETURNING * \
                  """
            params = {
                "name": document.name,
                "description": document.description,
                "file_path": document.file_path.as_posix(),
                "owner_id": get_ulid_to_string(document.owner_id),
                "group_id": get_ulid_to_string(document.group_id),
                "id": document_id,
            }
            await cur.execute(sql, params)
            return await cur.fetchone()


async def soft_delete_document_by_id(document_id: str) -> None:
    """
    Supprime un document de la BDD.
    """
    async with connection_async() as conn:
        async with conn.cursor() as cur:
            sql = "UPDATE documents SET deleted_at = NOW() WHERE id = %s"
            await cur.execute(sql, (document_id,))
