from datetime import datetime, timedelta
from typing import Optional

from app.core.cache import store_invitation_code, get_group_id_by_invitation_code, remove_invitation_code
from app.dao.groups import insert_group, select_all_groups, select_group_by_id, soft_delete_group, update_group
from app.dao.users_groups import add_user_to_group
from app.models.groups import format_groups_from_raw, format_group_from_raw
from app.schemas.groups import Group, GroupCreate, GroupInvitation


async def fetch_all_groups() -> list[Group]:
    """
    Affiche tous les groupes stockés dans la BDD.
    """
    raw_groups = await select_all_groups()
    return format_groups_from_raw(raw_groups)


async def fetch_group_by_id(group_id: str) -> Group:
    """
    Affiche un groupe stocké dans la BDD.
    """
    raw_group = await select_group_by_id(group_id)
    return format_group_from_raw(raw_group)


async def create_group(group: GroupCreate, user_id: str) -> Group:
    """
    Crée un groupe dans la BDD et y ajoute automatiquement le créateur.

    Args:
        group: Les données du groupe à créer.
        user_id: L'ID de l'utilisateur qui crée le groupe.

    Returns:
        Le groupe créé.
    """
    raw_group = await insert_group(group)
    group_obj = format_group_from_raw(raw_group)

    # Add the creator to the group
    await add_user_to_group(user_id, str(group_obj.id))

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

    Args:
        group_id: L'ID du groupe pour lequel créer une invitation.
        expiration_minutes: Le nombre de minutes avant l'expiration de l'invitation (par défaut: 24 heures).

    Returns:
        Un objet GroupInvitation contenant le code d'invitation et sa date d'expiration.
    """
    # Verify that the group exists
    group = await select_group_by_id(group_id)
    if not group:
        raise ValueError(f"Group {group_id} not found")

    # Generate and store the invitation code
    invitation_code = store_invitation_code(str(group_id), expiration_minutes)

    # Create and return the invitation object
    expires_at = datetime.utcnow() + timedelta(minutes=expiration_minutes)
    return GroupInvitation(
        group_id=group_id,
        invitation_code=invitation_code,
        expires_at=expires_at
    )


async def validate_group_invitation(invitation_code: str) -> Optional[Group]:
    """
    Valide un code d'invitation et retourne le groupe associé.

    Args:
        invitation_code: Le code d'invitation à valider.

    Returns:
        Le groupe associé au code d'invitation s'il est valide, None sinon.
    """
    # Get the group ID from the invitation code
    group_id = get_group_id_by_invitation_code(invitation_code)
    if not group_id:
        return None

    # Get the group from the database
    try:
        group = await fetch_group_by_id(group_id)
        return group
    except Exception:
        # If the group doesn't exist, remove the invitation code
        remove_invitation_code(invitation_code)
        return None


async def join_group_by_invitation(invitation_code: str, user_id: str) -> Optional[Group]:
    """
    Rejoint un groupe en utilisant un code d'invitation.

    Args:
        invitation_code: Le code d'invitation à utiliser.
        user_id: L'ID de l'utilisateur qui rejoint le groupe.

    Returns:
        Le groupe rejoint s'il est valide, None sinon.
    """
    # Validate the invitation code
    group = await validate_group_invitation(invitation_code)
    if not group:
        return None

    # Add the user to the group
    await add_user_to_group(user_id, str(group.id))

    return group
