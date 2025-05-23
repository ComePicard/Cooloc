from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies.auth import get_current_user
from app.schemas.auth import TokenData
from app.schemas.groups import Group, GroupCreate, GroupInvitation

from app.schemas.users import User
from app.services.groups import (
    remove_group, fetch_group_by_id, create_group, edit_group,
    create_group_invitation, validate_group_invitation, join_group_by_invitation, fetch_group_members,
    fetch_groups_for_user,
)

router = APIRouter()


@router.get(path="/me")
async def get_my_groups(current_user: TokenData = Depends(get_current_user)) -> list[Group]:
    """
    Récupère tous les groupes dont l'utilisateur courant est membre.
    """
    return await fetch_groups_for_user(current_user)


@router.get(path="/{group_id}")
async def get_group(group_id: str) -> Group:
    """
    Affiche un groupe stocké dans la BDD.
    """
    return await fetch_group_by_id(group_id)


@router.get(path='/{group_id}/members')
async def get_group_members(group_id: str) -> list[User]:
    """
    Récupère tous les utilisateurs membres d'un groupe.
    """
    return await fetch_group_members(group_id)


@router.post('/')
async def post_group(group: GroupCreate, current_user: TokenData = Depends(get_current_user)) -> Group:
    """
    Crée un groupe dans la BDD et y ajoute automatiquement le créateur.
    """
    return await create_group(group, current_user)


@router.patch('/{group_id}')
async def patch_group(group_id: str, group: GroupCreate) -> Group:
    """
    Modifie un groupe dans la BDD.
    """
    return await edit_group(group_id, group)


@router.delete('/{group_id}')
async def delete_group(group_id: str) -> str:
    """
    Supprime un groupe dans la BDD.
    """
    return await remove_group(group_id)


@router.post('/{group_id}/invitations')
async def create_invitation(group_id: str, current_user: TokenData = Depends(get_current_user)) -> GroupInvitation:
    """
    Crée un code d'invitation pour un groupe.
    """
    try:
        return await create_group_invitation(group_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get('/invitations/{invitation_code}')
async def validate_invitation(invitation_code: str, current_user: TokenData = Depends(get_current_user)) -> Group:
    """
    Valide un code d'invitation et retourne le groupe associé.
    """
    group = await validate_group_invitation(invitation_code)
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invalid or expired invitation code: {invitation_code}"
        )
    return group


@router.post('/invitations/{invitation_code}/join')
async def join_group(invitation_code: str, current_user: TokenData = Depends(get_current_user)) -> Group:
    """
    Rejoint un groupe en utilisant un code d'invitation.
    """
    group = await join_group_by_invitation(invitation_code, current_user)
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invalid or expired invitation code: {invitation_code}"
        )
    return group
