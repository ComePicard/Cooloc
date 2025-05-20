from fastapi import APIRouter, Depends

from app.dependencies.auth import get_current_user
from app.schemas.auth import TokenData
from app.schemas.groups import Group, GroupCreate
from app.services.groups import fetch_all_groups, remove_group, fetch_group_by_id, create_group, edit_group

router = APIRouter()


@router.get(path="/")
async def get_groups(current_user: TokenData = Depends(get_current_user)) -> list[Group]:
    """
    Affiche les groupes stockés dans la BDD.
    """
    return await fetch_all_groups()

@router.get(path="/{group_id}")
async def get_group(group_id: str, current_user: TokenData = Depends(get_current_user)) -> Group:
    """
    Affiche un groupe stocké dans la BDD.
    """
    return await fetch_group_by_id(group_id)


@router.post('/')
async def post_group(group: GroupCreate, current_user: TokenData = Depends(get_current_user)) -> Group:
    """
    Crée un groupe dans la BDD.
    """
    return await create_group(group)

@router.patch('/{group_id}')
async def patch_group(group_id: str, group: GroupCreate, current_user: TokenData = Depends(get_current_user)) -> Group:
    """
    Modifie un groupe dans la BDD.
    """
    return await edit_group(group_id, group)


@router.delete('/{group_id}')
async def delete_group(group_id: str, current_user: TokenData = Depends(get_current_user)) -> str:
    """
    Supprime un groupe dans la BDD.
    """
    return await remove_group(group_id)
