from pydantic import BaseModel, Field


class CartItems(BaseModel):
    qty: int = Field(gt=0)

    class Config:
        from_attributes = True
