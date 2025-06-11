from time_stamp import  TimeStampModel
from uuid import UUID
from enums import OrderStatus
from pydantic import Field


class Order(TimeStampModel):
    order_id: UUID
    cart_id: UUID
    customer_id: UUID
    total_price: float = Field(ge=0)
    order_status: OrderStatus
