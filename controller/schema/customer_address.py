from pydantic import BaseModel


class CustomerAddress(BaseModel):
    latitude: str
    longitude: str
    street: str
    pincode: str
    city: str
    flat_no: str

    class Config:
        from_attributes = True
