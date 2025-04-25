from datetime import datetime
from typing import Optional

from pydantic import SecretStr, Field
from pydantic_extra_types.ulid import ULID

from app.schemas.custom import BaseModelCustom

class UserCreate(BaseModelCustom):
    firstname: str = Field(..., title="First Name", max_length=50, description="First name of the user", examples=["John"])
    lastname: str = Field(..., title="Last Name", max_length=50, description="Last name of the user", examples=["Doe"])
    password: SecretStr = Field(..., title="Password", min_length=8, max_length=128, description="Password of the user", examples=["password123"])
    age: Optional[int] = Field(None, title="Age", ge=0, le=120, description="Age of the user", examples=[25])
    address: str = Field(..., title="Address", max_length=255, description="Address of the user", examples=["123 Main St"])
    phone_number: Optional[str] = Field(None, title="Phone Number", max_length=10, description="Phone number of the user", examples=["1234567890"])
    email: str = Field(..., title="Email", max_length=255, description="Email of the user", examples=["john-doe@example.com"])

class User(UserCreate):
    id: ULID
    updated_at: datetime
    deleted_at: Optional[datetime] = None