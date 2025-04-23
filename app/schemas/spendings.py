from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic_extra_types import ulid


class Spendings(BaseModel):
    id: ulid
    name: str
    description: Optional[str]
    amount: float
    currency: str
    updated_at: datetime
    owner_id: ulid
    group_id: ulid