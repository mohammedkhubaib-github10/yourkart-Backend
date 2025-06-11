from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from core.database import Base
from models.address_user_link import address_table


class Address(Base):
    __tablename__ = 'Addresses'
    address_id = Column(String(36), primary_key=True)
    street = Column(String(20))
    pincode = Column(String(10), nullable=False)
    city = Column(String(20))
    flat_no = Column(String(5))
    location = Column(String(100), nullable=False)
    vendor_id = Column(String(36), ForeignKey('Vendors.vendor_id'), nullable=False)

    customers = relationship('Customer', secondary=address_table, back_populates='addresses')

    vendor = relationship('Vendor', back_populates='shop_addresses')
