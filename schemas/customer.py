from user import User
from typing import List, Optional
from cart import Cart
from order import Order


class Customer(User):
    cart_items: Optional[List[Cart]]
    orders: Optional[List[Order]]
