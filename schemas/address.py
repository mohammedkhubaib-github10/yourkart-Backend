from uuid import UUID

from pydantic import BaseModel


class Address(BaseModel):
    location: str
    street: str
    pincode: str
    city: str
    flat_no: str
    vendor_id: UUID

    class Config:
        from_attributes = True
