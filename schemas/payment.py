from pydantic import Field
from time_stamp import TimeStampModel
from uuid import UUID
from enums import PaymentMode, PaymentStatus


class Payment(TimeStampModel):
    payment_id: UUID
    order_id: UUID
    payment_amount: float = Field(ge=0)
    payment_status: PaymentStatus
    payment_mode: PaymentMode
