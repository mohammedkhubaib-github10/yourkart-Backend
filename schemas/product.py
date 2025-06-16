from uuid import UUID

from pydantic import Field

from .time_stamp import TimeStampModel


class Product(TimeStampModel):
    product_name: str = Field(min_length=1)
    price: float = Field(ge=0)
    product_image: str

    class Config:
        from_attributes = True
