from fastapi import APIRouter

from app.schemas.groups import Group, GroupCreate
from app.services.groups import fetch_all_groups, remove_group, fetch_group_by_id, create_group, edit_group

router = APIRouter()


@router.get(path="/")
async def get_groups() -> list[Group]:
    """
    Affiche les groupes stockés dans la BDD.
    """
    return await fetch_all_groups()

@router.get(path="/{group_id}")
async def get_group(group_id: str) -> Group:
    """
    Affiche un groupe stocké dans la BDD.
    """
    return await fetch_group_by_id(group_id)


@router.post('/')
async def post_group(group: GroupCreate) -> Group:
    """
    Crée un groupe dans la BDD.
    """
    return await create_group(group)

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