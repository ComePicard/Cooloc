from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field
from pydantic_extra_types.ulid import ULID

from app.schemas.custom import BaseModelCustom


class SpendingReimbursementCreate(BaseModelCustom):
    spending_id: ULID = Field(..., title="Spending ID", description="ID of the spending being reimbursed",
                              examples=["01F8MECHZX3TBDSZ7XK4F8G5J6"])


class SpendingReimbursement(SpendingReimbursementCreate):
    reimbursement_amount: float = Field(..., title="Reimbursement Amount", ge=0, 
                                       description="Amount to be reimbursed by this user", 
                                       examples=[25.50])
    reimbursed_at: Optional[datetime] = Field(None, title="Reimbursed At", description="When the reimbursement was made")
    user_id: ULID = Field(..., title="User ID", description="ID of the user being reimbursed",
                          examples=["01F8MECHZX3TBDSZ7XK4F8G5J6"])

class ReimbursementSummary(BaseModelCustom):
    total_owed_by: float = Field(..., title="Total Owed By", ge=0, 
                                description="Total amount owed by the user", 
                                examples=[150.75])
    total_owed_to: float = Field(..., title="Total Owed To", ge=0, 
                               description="Total amount owed to the user", 
                               examples=[75.25])
    balance: float = Field(..., title="Balance", 
                         description="Net balance (positive means user is owed money, negative means user owes money)", 
                         examples=[-75.50])
