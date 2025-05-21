from psycopg2.extras import RealDictRow

from app.schemas.groups import Group


def format_group_from_raw(raw_group: RealDictRow) -> Group:
    """
    Formate les groupes bruts en objets Group.
    """
    return Group(**raw_group)


def format_groups_from_raw(raw_groups: list[RealDictRow]) -> list[Group]:
    """
    Formate les groupes bruts en objets Group.
    """
    return [format_group_from_raw(raw_group) for raw_group in raw_groups]
