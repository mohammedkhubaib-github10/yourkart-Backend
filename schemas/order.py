from uuid import UUID

from pydantic import Field

from .enums import OrderStatus
from .time_stamp import TimeStampModel


class Order(TimeStampModel):
    order_status: OrderStatus
    delivery_address_id: str

    class Config:
        from_attributes = True
