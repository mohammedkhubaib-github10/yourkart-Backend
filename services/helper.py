from math import radians, sin, cos, sqrt, asin

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


def haversine(lat1, lon1, lat2, lon2):
    lat1 = float(lat1)
    lat2 = float(lat2)
    lon1 = float(lon1)
    lon2 = float(lon2)
    R = 6371  # Earth radius in kilometers

    d_lat = radians(lat2 - lat1)
    d_lon = radians(lon2 - lon1)

    a = sin(d_lat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(d_lon / 2) ** 2
    c = 2 * asin(sqrt(a))

    return R * c  # distance in km
