import uuid

from sqlalchemy import Column, ForeignKey, String, Integer, Float
from sqlalchemy.orm import relationship

from core.database import Base


class Cart(Base):
    __tablename__ = 'Carts'
    cart_id = Column(String(36), primary_key=True, default=uuid.uuid4())
    customer_id = Column(String(36), ForeignKey('Customers.customer_id'), nullable=False)

    customer = relationship('Customer', back_populates='cart', uselist=False)
    items = relationship('CartItem', back_populates='cart', cascade='all, delete-orphan')
    order = relationship('Order', back_populates='cart', uselist=False)


class CartItem(Base):
    __tablename__ = 'Cart_Items'
    item_id = Column(String(36), primary_key=True, default= lambda: str(uuid.uuid4()))
    qty = Column(Integer, nullable=False, default=1)
    total_price = Column(Float, nullable=False)
    cart_id = Column(String(36), ForeignKey('Carts.cart_id'), nullable=False)
    product_id = Column(String(36), ForeignKey('Products.product_id'), nullable=False)

    product = relationship('Product', back_populates='cart_items')
    cart = relationship('Cart', back_populates='items')

