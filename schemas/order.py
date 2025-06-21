from uuid import UUID

from pydantic import Field

from .enums import OrderStatus
from .time_stamp import TimeStampModel


class Order(TimeStampModel):
    order_status: OrderStatus

    class Config:
        from_attributes = True
