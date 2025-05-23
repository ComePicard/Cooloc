from datetime import datetime, timedelta
from typing import Optional

from app.core.cache import store_invitation_code, get_group_id_by_invitation_code, remove_invitation_code
from app.dao.groups import insert_group, select_group_by_id, soft_delete_group, update_group
from app.dao.users_groups import add_user_to_group, get_groups_for_user, get_users_in_group
from app.models.groups import format_groups_from_raw, format_group_from_raw
from app.models.users import format_users_from_raw
from app.schemas.auth import TokenData
from app.schemas.groups import Group, GroupCreate, GroupInvitation
from app.schemas.users import User
from app.services.users import fetch_user_by_email


async def fetch_group_by_id(group_id: str) -> Group:
    """
    Affiche un groupe stocké dans la BDD.
    """
    raw_group = await select_group_by_id(group_id)
    return format_group_from_raw(raw_group)


async def fetch_groups_for_user(current_user: TokenData) -> list[Group]:
    """
    Récupère tous les groupes dont l'utilisateur courant est membre.
    """
    owner = await fetch_user_by_email(current_user.email)
    raw_groups = await get_groups_for_user(owner.id)
    return format_groups_from_raw(raw_groups)


async def fetch_group_members(group_id: str) -> list[User]:
    """
    Récupère tous les utilisateurs membres d'un groupe.
    """
    group = await fetch_group_by_id(group_id)
    if not group:
        raise ValueError(f"Group with ID {group_id} not found")
    request = await get_users_in_group(group_id)
    return format_users_from_raw(request)


async def create_group(group: GroupCreate, current_user: TokenData) -> Group:
    """
    Crée un groupe dans la BDD et y ajoute automatiquement le créateur.
    """
    owner = await fetch_user_by_email(current_user.email)
    raw_group = await insert_group(group)
    group_obj = format_group_from_raw(raw_group)

    await add_user_to_group(owner.id, str(group_obj.id))

    return group_obj


async def edit_group(group_id: str, group: GroupCreate) -> Group:
    """
    Modifie un groupe dans la BDD.
    """
    raw_group = await update_group(group_id, group)
    return format_group_from_raw(raw_group)


async def remove_group(group_id: str) -> str:
    """
    Supprime un groupe dans la BDD.
    """
    group = await select_group_by_id(group_id)
    if group:
        await soft_delete_group(group_id)
        return f"Group {group_id} deleted"
    return f"Group {group_id} not found"


async def create_group_invitation(group_id: str, expiration_minutes: int = 60 * 24) -> GroupInvitation:
    """
    Crée une invitation pour un groupe avec un code à 8 chiffres.
    """
    group = await select_group_by_id(group_id)
    if not group:
        raise ValueError(f"Group {group_id} not found")

    invitation_code = store_invitation_code(str(group_id), expiration_minutes)

    expires_at = datetime.utcnow() + timedelta(minutes=expiration_minutes)
    return GroupInvitation(
        group_id=group_id,
        invitation_code=invitation_code,
        expires_at=expires_at
    )


async def validate_group_invitation(invitation_code: str) -> Optional[Group]:
    """
    Valide un code d'invitation et retourne le groupe associé.
    """
    group_id = get_group_id_by_invitation_code(invitation_code)
    if not group_id:
        return None

    try:
        group = await fetch_group_by_id(group_id)
        return group
    except Exception:
        remove_invitation_code(invitation_code)
        return None


async def join_group_by_invitation(invitation_code: str, current_user: TokenData) -> Optional[Group]:
    """
    Rejoint un groupe en utilisant un code d'invitation.
    """
    owner = await fetch_user_by_email(current_user.email)
    group = await validate_group_invitation(invitation_code)
    if not group:
        return None
    await add_user_to_group(owner.id, str(group.id))
    return group
