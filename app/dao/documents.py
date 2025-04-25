from psycopg2.extras import RealDictRow

from app.db.settings import connection_async
from app.schemas.documents import Documents, DocumentsCreate
from app.utils.schemas import get_ulid_to_string


async def select_document_by_id(document_id: int) -> RealDictRow:
    """
    Affiche un document stocké dans la BDD.
    """
    async with connection_async() as conn:
        async with conn.cursor() as cur:
            sql = "SELECT * FROM Documents WHERE id = %s"
            params = {"document_id": document_id}
            await cur.execute(sql, params)
            return await cur.fetchone()


async def select_documents_by_group(group_id: str) -> RealDictRow:
    """
    Affiche les documents stockés dans la BDD.
    """
    async with connection_async() as conn:
        async with conn.cursor() as cur:
            sql = "SELECT * FROM Documents WHERE group_id = %s"
            params = {"group_id": group_id}
            await cur.execute(sql, params)
            return await cur.fetchall()


async def select_documents_by_user(user: str) -> RealDictRow:
    """
    Affiche les documents stockés dans la BDD.
    """
    async with connection_async() as conn:
        async with conn.cursor() as cur:
            sql = "SELECT * FROM Documents WHERE group_id = %s"
            params = {"user_id": user}
            await cur.execute(sql, params)
            return await cur.fetchall()


async def insert_document(document: DocumentsCreate) -> RealDictRow:
    """
    Crée un document dans la BDD.
    """
    async with connection_async() as conn:
        async with conn.cursor() as cur:
            sql = """
                INSERT INTO Documents (
                    name,
                    description,
                    file_path,
                    owner_id,
                    group_id
                )
                VALUES (
                    %(name)s, 
                    %(description)s, 
                    %(file_path)s, 
                    %(owner_id)s, 
                    %(group_id)s
               ) RETURNING *
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


async def update_document_by_id(document_id: str, document: DocumentsCreate) -> RealDictRow:
    """
    Met à jour un document dans la BDD.
    """
    async with connection_async() as conn:
        async with conn.cursor() as cur:
            sql = """
                UPDATE Documents
                SET 
                    name = %(name)s,
                    description = %(description)s,
                    file_path = %(file_path)s,
                    owner_id = %(owner_id)s,
                    group_id = %(group_id)s
                  WHERE id = %(id)s
                  RETURNING *
                  """
            params = {
                "name": document.name,
                "description": document.description,
                "file_path": document.file_path,
                "owner_id": get_ulid_to_string(document.owner_id),
                "group_id": get_ulid_to_string(document.group_id),
                "id": document_id,
            }
            await cur.execute(sql, params)
            return await cur.fetchone()


async def soft_delete_document_by_id(document_id: int) -> None:
    """
    Supprime un document de la BDD.
    """
    async with connection_async() as conn:
        async with conn.cursor() as cur:
            sql = "UPDATE deleted_at=NOW() FROM documents WHERE id = %(id)s"
            params = {"id": document_id}
            await cur.execute(sql, params)