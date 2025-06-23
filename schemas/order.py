from uuid import UUID

from pydantic import Field

from .enums import OrderStatus, PaymentMode
from .time_stamp import TimeStampModel


class Order(TimeStampModel):
    payment_mode: PaymentMode
    delivery_address_id: str

    class Config:
        from_attributes = True
