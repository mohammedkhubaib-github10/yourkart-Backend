import uuid

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from core.database import Base


class CustomerAddress(Base):
    __tablename__ = 'Customer_Addresses'
    address_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    street = Column(String(20))
    pincode = Column(String(10), nullable=False)
    city = Column(String(20))
    flat_no = Column(String(5))
    location = Column(String(100), nullable=False)
    customer_id = Column(String(36), ForeignKey('Customers.customer_id'), nullable=False)

    customer = relationship('Customer', back_populates='addresses')


class VendorAddress(Base):
    __tablename__ = 'Vendor_Addresses'
    address_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    street = Column(String(20))
    pincode = Column(String(10), nullable=False)
    city = Column(String(20))
    location = Column(String(100), nullable=False)
    vendor_id = Column(String(36), ForeignKey('Vendors.vendor_id'), nullable=False)

    vendor = relationship('Vendor', back_populates='shop_addresses')
