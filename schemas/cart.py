from uuid import UUID

from pydantic import BaseModel


class Cart(BaseModel):
    cart_id: UUID
    customer_id: UUID
