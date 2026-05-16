from pydantic import Field, EmailStr, BaseModel


class Customer(BaseModel):
    customer_name: str = Field(min_length=1)
    email: EmailStr

    class Config:
        from_attributes = True
