from uuid import UUID

from pydantic import BaseModel, Field


class CartItems(BaseModel):
    qty: int = Field(gt=0)
    total_price: float = Field(ge=0)
    cart_id: UUID
    product_id: UUID

    class Config:
        from_attributes = True