from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic_extra_types import ulid


class SpendingsCreate(BaseModel):
    name: str
    description: Optional[str]
    amount: float
    currency: str
    owner_id: ulid
    group_id: ulid

class Spendings(SpendingsCreate):
    id: ulid
    updated_at: datetime