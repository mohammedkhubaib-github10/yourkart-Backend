from pydantic import BaseModel

from controller.enums.enums import PaymentMode


class Order(BaseModel):
    payment_mode: PaymentMode
    delivery_address_id: str

    class Config:
        from_attributes = True
