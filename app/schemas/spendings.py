from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field
from pydantic_extra_types.ulid import ULID

from app.schemas.custom import BaseModelCustom


class SpendingCreate(BaseModelCustom):
    name: str = Field(..., title="Name", max_length=50, description="Name of the spending", examples=["Groceries"])
    description: Optional[str] = Field(None, title="Description", max_length=255, description="Description of the spending", examples=["Weekly groceries"])
    amount: float = Field(..., title="Amount", ge=0, description="Amount of the spending", examples=[100.50])
    currency: str = Field(..., title="Currency", max_length=3, description="Currency of the spending", examples=["EUR"])
    is_reimbursed: bool = Field(False, title="Is Reimbursed", description="Whether the spending has been reimbursed")
    group_id: ULID = Field(None, title="Group ID", description="ID of the group associated with the spending", examples=["01F8MECHZX3TBDSZ7XK4F8G5J6"])

class Spending(SpendingCreate):
    id: ULID
    updated_at: datetime
    deleted_at: Optional[datetime] = None
    owner_id: ULID = Field(..., title="Owner ID", description="ID of the user who owns the spending",
                           examples=["01F8MECHZX3TBDSZ7XK4F8G5J6"])