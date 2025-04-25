from datetime import datetime
from typing import Optional

from pydantic import Field
from pydantic_extra_types.ulid import ULID

from app.schemas.custom import BaseModelCustom


class GroupCreate(BaseModelCustom):
    name: str = Field(..., title="Name", max_length=50, description="Name of the group", examples=["Roommates"])
    description: Optional[str] = Field(None, title="Description", max_length=255, description="Description of the group", examples=["Group of roommates sharing expenses"])
    city: str = Field(..., title="City", max_length=50, description="City of the group", examples=["Rennes"])
    postal_code: str = Field(..., title="Postal Code", max_length=10, description="Postal code of the group", examples=["35000"])
    country: str = Field(..., title="Country", max_length=50, description="Country of the group", examples=["France"])
    contact_email: Optional[str] = Field(None, title="Contact Email", max_length=255, description="Contact email of the property owner", examples=["property-owner@example.com"])
    contact_phone: Optional[str] = Field(None, title="Contact Phone", max_length=15, description="Contact phone number of the property owner", examples=["0123456789"])
    agency_email: Optional[str] = Field(None, title="Agency Email", max_length=255, description="Contact email of the agency", examples=["agency@example.com"])
    agency_phone: Optional[str] = Field(None, title="Agency Phone", max_length=15, description="Contact phone number of the agency", examples=["0123456789"])
    starting_at: datetime = Field(..., title="Starting At", description="Starting date of the group", examples=["2023-01-01T00:00:00Z"])
    ending_at: Optional[datetime] = Field(None, title="Ending At", description="Ending date of the group", examples=["2023-12-31T23:59:59Z"])

class Group(GroupCreate):
    id: ULID
    updated_at: datetime
    deleted_at: Optional[datetime] = None