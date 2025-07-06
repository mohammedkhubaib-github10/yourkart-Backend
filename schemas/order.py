from pydantic import BaseModel

from pydantic import BaseModel

from .enums import PaymentMode


class Order(BaseModel):
    payment_mode: PaymentMode
    delivery_address_id: str

    class Config:
        from_attributes = True
