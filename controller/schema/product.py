from pydantic import Field, BaseModel


class Product(BaseModel):
    product_name: str = Field(min_length=1)
    price: float = Field(ge=0)
    product_image: str

    class Config:
        from_attributes = True
