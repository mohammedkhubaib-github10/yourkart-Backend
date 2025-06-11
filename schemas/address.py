from pydantic import BaseModel
from uuid import  UUID


class Address(BaseModel):
    address_id: UUID
    location: str
    street: str
    pincode: str
    city: str
    flat_no: str
    vendor_id: UUID