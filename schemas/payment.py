from pydantic import Field
from time_stamp import TimeStampModel
from uuid import UUID


class Payment(TimeStampModel):
    id: UUID
    order_id: UUID
    total_price: float = Field(ge=0)
    payment_status: bool = False