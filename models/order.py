import uuid

from sqlalchemy import Column, String, Float, ForeignKey, DATETIME, Integer
from sqlalchemy.orm import relationship

from core.database import Base


class Order(Base):
    __tablename__ = 'Orders'
    order_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    total_price = Column(Float, nullable=False)
    order_status = Column(String(20), nullable=False)
    delivery_address_id = Column(String(36), ForeignKey("Customer_Addresses.address_id", ondelete="CASCADE"),
                                 nullable=False)
    customer_id = Column(String(36), ForeignKey('Customers.customer_id'), nullable=False)
    cart_id = Column(String(36), ForeignKey('Carts.cart_id'), nullable=False)
    created_at = Column(DATETIME, nullable=False)

    delivery_address = relationship("CustomerAddress")
    customer = relationship('Customer', back_populates='orders')
    cart = relationship('Cart', back_populates='order', uselist=False)
    payment = relationship('Payment', back_populates='order', uselist=False)
    items = relationship('OrderItem', back_populates='order', cascade='all, delete-orphan')


class OrderItem(Base):
    __tablename__ = 'Order_Items'
    item_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    order_id = Column(String(36), ForeignKey('Orders.order_id'), nullable=False)
    product_id = Column(String(36), ForeignKey('Products.product_id'), nullable=False)
    qty = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)

    order = relationship('Order', back_populates='items')
    product = relationship('Product')
