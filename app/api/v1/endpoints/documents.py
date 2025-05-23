from fastapi import APIRouter, Depends

from app.dependencies.auth import get_current_user
from app.schemas.auth import TokenData
from app.schemas.documents import Document, DocumentCreate
from app.services.documents import fetch_documents_by_group, fetch_document_by_id, create_document, \
    remove_document, fetch_documents_by_user
from app.services.users import fetch_user_by_email

router = APIRouter()


@router.get(path="/{document_id}")
async def get_document_by_id(document_id: str) -> Document | None:
    """
    Affiche un document stocké dans la BDD.
    """
    return await fetch_document_by_id(document_id)


@router.get(path="/{group_id}")
async def get_documents_by_group(group_id: str) -> list[Document]:
    """
    Affiche les documents par groupe stockés dans la BDD.
    """
    return await fetch_documents_by_group(group_id)


@router.get(path="/{user_id}")
async def get_documents_by_user(user_id: str) -> list[Document]:
    """
    Affiche les documents par utilisateur stockés dans la BDD.
    """
    return await fetch_documents_by_user(user_id)


@router.post(path="/")
async def post_document(document: DocumentCreate,
                        current_user: TokenData = Depends(get_current_user)) -> Document | None:
    """
    Crée un document dans la BDD.
    """
    owner = await fetch_user_by_email(current_user.email)
    document.owner_id = owner.id
    return await create_document(document)


@router.delete(path="/{document_id}")
async def delete_document(document_id: str) -> str:
    """
    Supprime un document dans la BDD.
    """
    return await remove_document(document_id)
