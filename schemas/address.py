from uuid import UUID

from pydantic import BaseModel


class Address(BaseModel):
    address_id: UUID
    location: str
    street: str
    pincode: str
    city: str
    flat_no: str
    vendor_id: UUID
