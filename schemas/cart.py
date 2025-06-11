from pydantic import BaseModel, Field
from uuid import UUID


class Cart(BaseModel):
    cart_id: UUID
    customer_id: UUID