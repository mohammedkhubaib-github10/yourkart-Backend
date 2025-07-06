from pydantic import Field, EmailStr, BaseModel


class Vendor(BaseModel):
    vendor_name: str = Field(min_length=1)
    email: EmailStr
    brand_name: str = Field(min_length=1)

    class Config:
        from_attributes = True
