from pydantic import BaseModel


class VendorAddress(BaseModel):
    street: str
    pincode: str
    city: str
    latitude: str
    longitude: str

    class Config:
        from_attributes = True
