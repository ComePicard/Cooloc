from datetime import datetime

from pydantic import BaseModel, Field
from pydantic_extra_types.ulid import ULID

from app.schemas.custom import BaseModelCustom


class SpendingReimbursementCreate(BaseModelCustom):
    spending_id: ULID = Field(..., title="Spending ID", description="ID of the spending being reimbursed",
                              examples=["01F8MECHZX3TBDSZ7XK4F8G5J6"])


class SpendingReimbursement(SpendingReimbursementCreate):
    reimbursed_at: datetime = Field(..., title="Reimbursed At", description="When the reimbursement was made")
    user_id: ULID = Field(..., title="User ID", description="ID of the user being reimbursed",
                          examples=["01F8MECHZX3TBDSZ7XK4F8G5J6"])
