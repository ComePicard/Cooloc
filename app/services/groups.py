from app.dao.groups import insert_group, select_all_groups, select_group_by_id, soft_delete_group, update_group
from app.models.groups import format_groups_from_raw, format_group_from_raw
from app.schemas.groups import Group, GroupCreate


async def fetch_all_groups() -> list[Group]:
    """
    Affiche tout les groupes stockés dans la BDD.
    """
    raw_groups = await select_all_groups()
    return format_groups_from_raw(raw_groups)


async def fetch_group_by_id(group_id: str) -> Group:
    """
    Affiche un groupe stocké dans la BDD.
    """
    raw_group = await select_group_by_id(group_id)
    return format_group_from_raw(raw_group)


async def create_group(group: GroupCreate) -> Group:
    """
    Crée un groupe dans la BDD.
    """
    raw_group = await insert_group(group)
    return format_group_from_raw(raw_group)


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