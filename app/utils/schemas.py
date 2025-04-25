from typing import Optional

from pydantic_extra_types.ulid import ULID


def get_ulid_to_string(entry: Optional[ULID]) -> str | None:
    """
    Convertit un champ de type Field en chaîne de caractères.
    """
    return str(entry) if entry else None