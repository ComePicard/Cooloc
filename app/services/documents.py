from psycopg2.extras import RealDictRow

from app.dao.documents import select_documents_by_group, select_document_by_id, select_documents_by_user, \
    insert_document
from app.models.documents import format_documents_from_raw, format_document_from_raw
from app.schemas.documents import Documents, DocumentsCreate


async def fetch_document_by_id(document_id) -> Documents:
    """
    Affiche un document stocké dans la BDD.
    """
    raw_document = await select_document_by_id(document_id)
    document = format_document_from_raw(raw_document)
    return document


async def fetch_documents_by_group(group_id: str) -> list[Documents]:
    """
    Affiche les documents stockés dans la BDD.
    """
    raw_documents = await select_documents_by_group(group_id)
    documents = format_documents_from_raw(raw_documents)
    return documents


async def fetch_documents_by_user(user: str) -> list[Documents]:
    """
    Affiche les documents stockés dans la BDD.
    """
    raw_documents = await select_documents_by_user(user)
    documents = format_documents_from_raw(raw_documents)
    return documents


async def create_document(document: DocumentsCreate) -> Documents:
    """
    Crée un document dans la BDD.
    """
    raw_document = await insert_document(document)
    document = format_document_from_raw(raw_document)
    return document

async def edit_document(document_id: int, document: DocumentsCreate) -> Documents:
    """
    Modifie un document dans la BDD.
    """
    raw_document = await insert_document(document)
    document = format_document_from_raw(raw_document)
    return document


async def remove_document(document_id: int) -> str:
    """
    Supprime un document dans la BDD.
    """
    document = await select_document_by_id(document_id)
    if not document:
        return f"Document {document_id} not found"
    return f"Document {document_id} deleted"