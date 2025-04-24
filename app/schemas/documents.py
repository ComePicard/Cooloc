from datetime import datetime
from pathlib import Path
from typing import Optional

from pydantic import BaseModel
from pydantic_extra_types import ulid


class DocumentsCreate(BaseModel):
    name: str
    description: Optional[str]
    file_path: Path
    owner_id: ulid
    group_id: Optional[ulid]

class Documents(DocumentsCreate):
    id: ulid
    updated_at: datetime
