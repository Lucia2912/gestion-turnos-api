from pydantic import BaseModel
from typing import Optional

class PaymentOut(BaseModel):
    status: str
    transaction_id: Optional[str]
    message: str