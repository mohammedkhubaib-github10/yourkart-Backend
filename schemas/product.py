from time_stamp import TimeStampModel
from uuid import UUID
from pydantic import Field
from typing import Optional


class Product(TimeStampModel):
    product_id: UUID
    vendor_id: UUID
    product_name: str = Field(min_length=1)
    price: float = Field(ge=0)
    product_image: str
