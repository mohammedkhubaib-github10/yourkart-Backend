from uuid import UUID

from pydantic import BaseModel


class Cart(BaseModel):
    customer_id: UUID

    class Config:
        from_attributes = True
