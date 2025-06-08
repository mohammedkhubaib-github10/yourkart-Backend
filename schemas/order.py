from time_stamp import  TimeStampModel
from uuid import UUID
from enums import PaymentMode, OrderStatus
from pydantic import Field


class Order(TimeStampModel):
    id: UUID
    product_id: UUID
    customer_id: UUID
    total_price: float = Field(ge=0)
    payment_mode: PaymentMode
    order_status: OrderStatus