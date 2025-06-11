from pydantic import Field, EmailStr
from uuid import UUID
from time_stamp import TimeStampModel


class Vendor(TimeStampModel):
    vendor_id: UUID
    vendor_name: str = Field(min_length=1)
    email: EmailStr
    contact: str = Field(min_length=10, max_length=10)
    brand_name: str = Field(min_length=1)
