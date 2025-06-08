from pydantic import BaseModel
from uuid import  UUID


class Address(BaseModel):
    address_id: UUID
    street: str
    pincode: str
    city: str
    flat_no: str
    lives: UUID