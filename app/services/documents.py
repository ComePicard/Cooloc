from app.dao.documents import select_documents_by_group, select_document_by_id, select_documents_by_user, \
    insert_document, soft_delete_document_by_id
from app.models.documents import format_documents_from_raw, format_document_from_raw
from app.schemas.documents import Document, DocumentCreate


async def fetch_document_by_id(document_id: str) -> Document | None:
    """
    Affiche un document stocké dans la BDD.
    """
    raw_document = await select_document_by_id(document_id)
    document = format_document_from_raw(raw_document)
    return document


async def fetch_documents_by_group(group_id: str) -> list[Document]:
    """
    Affiche les documents par groupe stockés dans la BDD.
    """
    raw_documents = await select_documents_by_group(group_id)
    documents = format_documents_from_raw(raw_documents)
    return documents


async def fetch_documents_by_user(user_id: str) -> list[Document]:
    """
    Affiche les documents par utilisateur stockés dans la BDD.
    """
    raw_documents = await select_documents_by_user(user_id)
    documents = format_documents_from_raw(raw_documents)
    return documents


async def create_document(document: DocumentCreate) -> Document | None:
    """
    Crée un document dans la BDD.
    """
    raw_document = await insert_document(document)
    document = format_document_from_raw(raw_document)
    return document


async def remove_document(document_id: str) -> str:
    """
    Supprime un document dans la BDD.
    """
    document = await select_document_by_id(document_id)
    if not document:
        return f"Document {document_id} not found"
    await soft_delete_document_by_id(document_id)
    return f"Document {document_id} deleted"
