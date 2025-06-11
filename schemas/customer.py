from uuid import UUID

from pydantic import Field, EmailStr

from time_stamp import TimeStampModel


class Customer(TimeStampModel):
    customer_id: UUID
    customer_name: str = Field(min_length=1)
    email: EmailStr
    contact: str = Field(min_length=10, max_length=10)
