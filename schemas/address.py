from pydantic import BaseModel


class VendorAddress(BaseModel):
    street: str
    pincode: str
    city: str
    latitude: str
    longitude: str

    class Config:
        from_attributes = True


class CustomerAddress(BaseModel):
    latitude: str
    longitude: str
    street: str
    pincode: str
    city: str
    flat_no: str

    class Config:
        from_attributes = True
