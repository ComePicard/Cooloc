from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic_extra_types import ulid


class GroupsCreate(BaseModel):
    name: str
    description: Optional[str]
    city: str
    postal_code: str
    country: str
    contact_email: Optional[str]
    contact_phone: Optional[str]
    agency_email: Optional[str]
    agency_phone: Optional[str]
    starting_at: datetime
    ending_at: Optional[datetime]

class Groups(GroupsCreate):
    id: ulid
    updated_at: datetime