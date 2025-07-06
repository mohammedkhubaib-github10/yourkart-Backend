from pydantic import BaseModel, Field


class Cart(BaseModel):
    amount: float = Field(ge=0)

    class Config:
        from_attributes = True
