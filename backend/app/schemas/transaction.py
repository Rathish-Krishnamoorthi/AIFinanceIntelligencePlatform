from typing import Optional
from pydantic import BaseModel, Field


class TransactionCreate(BaseModel):
    date: str
    amount: float = Field(gt=0)
    transaction_type: str
    category: str
    description: str = ""
    vendor_id: Optional[str] = None
    vendor_name: Optional[str] = None
    account: str = "Operating"
    payment_method: str = "Bank transfer"
    currency: str = "INR"
    status: str = "COMPLETED"
    department: Optional[str] = None
