from pydantic import BaseModel, Field
from uuid import UUID


class Cart(BaseModel):
    id: UUID
    product_id: UUID
    customer_id: UUID
    qty: int = Field(gt=0)