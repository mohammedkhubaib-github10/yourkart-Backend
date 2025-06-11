from uuid import UUID

from pydantic import Field

from enums import OrderStatus
from time_stamp import TimeStampModel


class Order(TimeStampModel):
    order_id: UUID
    cart_id: UUID
    customer_id: UUID
    total_price: float = Field(ge=0)
    order_status: OrderStatus
