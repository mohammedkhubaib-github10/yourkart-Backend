from uuid import UUID

from pydantic import Field, BaseModel

from .enums import PaymentMode, PaymentStatus


class Payment(BaseModel):
    order_id: UUID
    payment_amount: float = Field(ge=0)
    payment_status: PaymentStatus
    payment_mode: PaymentMode

    class Config:
        from_attributes = True
