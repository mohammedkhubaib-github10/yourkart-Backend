from pydantic import BaseModel, Field
from uuid import UUID


class CartItems(BaseModel):
    item_id: UUID
    qty: int = Field(gt=0)
    total_price: float = Field(ge=0)
    cart_id: UUID
    product_id: UUID