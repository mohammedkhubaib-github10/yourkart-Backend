from sqlalchemy.orm import Session

import models


def update_cart_amount(cart_id: str, item_price: float, db: Session, add: bool):
    cart = db.query(models.Cart).filter(models.Cart.cart_id == cart_id).first()
    if cart:
        if add:
            cart.amount += item_price
        else:
            cart.amount = max(0, cart.amount - item_price)

        db.commit()
