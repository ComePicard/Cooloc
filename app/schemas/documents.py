from datetime import datetime
from pathlib import Path
from typing import Optional

from pydantic import BaseModel
from pydantic_extra_types import ulid


class Documents(BaseModel):
    id: ulid
    name: str
    description: Optional[str]
    file_path: Path
    updated_at: datetime
    owner_id: ulid
    group_id: Optional[ulid]