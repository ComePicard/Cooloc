from datetime import datetime
from typing import Optional

from pydantic import BaseModel, SecretStr
from pydantic_extra_types import ulid


class Users(BaseModel):
    id: ulid
    firstname: str
    lastname: str
    password: SecretStr
    age: Optional[int]
    adress: str
    phone_number: Optional[str]
    email: str
    updated_at: datetime