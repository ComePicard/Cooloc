from fastapi import APIRouter

from app.schemas.documents import Documents, DocumentsCreate
from app.services.documents import fetch_documents_by_group, fetch_document_by_id, create_document, edit_document, \
    remove_document

router = APIRouter()


@router.get(path="/{document_id}")
async def get_document_by_id(document_id: int) -> Documents:
    """
    Affiche un document stocké dans la BDD.
    """
    return fetch_document_by_id(document_id)


@router.get(path="/{group_id}")
async def get_documents_by_group(group_id: str) -> list[Documents]:
    """
    Affiche les utilisateurs stockés dans la BDD.
    """
    return fetch_documents_by_group(group_id)


@router.get(path="/{user_id}")
async def get_documents_by_user(user_id: str) -> list[Documents]:
    """
    Affiche les utilisateurs stockés dans la BDD.
    """
    return fetch_documents_by_group(user_id)


@router.post(path="/")
async def post_document(document: DocumentsCreate) -> Documents:
    """
    Crée un document dans la BDD.
    """
    return await create_document(document)


@router.patch(path="/{document_id}")
async def patch_document(document_id: int, document: DocumentsCreate) -> Documents:
    """
    Modifie un document dans la BDD.
    """
    return await edit_document(document_id, document)


@router.delete(path="/{document_id}")
async def delete_document(document_id: int) -> str:
    """
    Supprime un document dans la BDD.
    """
    return await remove_document(document_id)