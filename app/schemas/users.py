from datetime import datetime
from typing import Optional

from pydantic import BaseModel, SecretStr, Field
from pydantic_extra_types import ulid


class UsersCreate(BaseModel):
    firstname: str = Field(..., title="First Name", max_length=50, description="First name of the user", examples=["John"])
    lastname: str
    password: SecretStr
    age: Optional[int]
    address: str
    phone_number: Optional[str]
    email: str

class Users(UsersCreate):
    id: ulid.ULID
    updated_at: datetime