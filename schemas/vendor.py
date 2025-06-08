from user import User
from typing import List, Optional
from product import Product
from pydantic import Field
from order import Order


class Vendor(User):
    store_name: str = Field(min_length=1)
    inventory: Optional[List[Product]]
    order_received: List[Order] = []