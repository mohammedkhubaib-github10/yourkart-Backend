from time_stamp import TimeStampModel
from uuid import UUID
from pydantic import Field, EmailStr
from typing import List
from address import Address


class User(TimeStampModel):
    id: UUID
    name: str = Field(min_length=1)
    email: EmailStr
    contact: str = Field(min_length=10, max_length=10)
    location: str = Field(min_length=1)
    address: Address
