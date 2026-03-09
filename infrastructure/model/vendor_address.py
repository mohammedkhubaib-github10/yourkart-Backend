import uuid

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from infrastructure.database.session import Base


class VendorAddress(Base):
    __tablename__ = 'Vendor_Addresses'
    address_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    street = Column(String(100))
    pincode = Column(String(10), nullable=False)
    city = Column(String(100))
    latitude = Column(String(100), nullable=True)
    longitude = Column(String(100), nullable=True)
    vendor_id = Column(String(36), ForeignKey('Vendors.vendor_id'), nullable=False)

    vendor = relationship('Vendor', back_populates='shop_addresses')
