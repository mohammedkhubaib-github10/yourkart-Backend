from pydantic import BaseModel


class VendorAddress(BaseModel):
    location: str
    street: str
    pincode: str
    city: str

    class Config:
        from_attributes = True


class CustomerAddress(BaseModel):
    location: str
    street: str
    pincode: str
    city: str
    flat_no: str

    class Config:
        from_attributes = True
