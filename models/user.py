import uuid

from sqlalchemy import Column, String, DATETIME
from sqlalchemy.orm import relationship

from core.database import Base


class Customer(Base):
    __tablename__ = 'Customers'
    customer_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    customer_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True)
    contact = Column(String(10), unique=True)
    created_at = Column(DATETIME, nullable=False)

    addresses = relationship('CustomerAddress', back_populates='customer', cascade='all, delete-orphan')
    cart = relationship('Cart', back_populates='customer', cascade='all, delete-orphan', uselist=False)
    orders = relationship('Order', back_populates='customer', cascade='all, delete-orphan')


class Vendor(Base):
    __tablename__ = 'Vendors'
    vendor_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    vendor_name = Column(String(100), nullable=False)
    brand_name = Column(String(100), unique=True, nullable=False)
    email = Column(String(100), unique=True)
    contact = Column(String(10), unique=True)
    created_at = Column(DATETIME, nullable=False)

    shop_addresses = relationship('VendorAddress', back_populates='vendor', cascade='all, delete-orphan')
    products = relationship('Product', back_populates='vendor', cascade='all, delete-orphan')
