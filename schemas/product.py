from time_stamp import TimeStampModel
from uuid import UUID
from pydantic import Field
from typing import Optional


class Product(TimeStampModel):
    id: UUID
    vendor_id: UUID
    name: str = Field(min_length=1)
    price: float = Field(ge=0)
    description: Optional[str] = None
    image: str
