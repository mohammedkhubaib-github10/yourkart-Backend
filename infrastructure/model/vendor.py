import uuid

from sqlalchemy import Column, String, DATETIME
from sqlalchemy.orm import relationship

from infrastructure.database.session import Base


class Vendor(Base):
    __tablename__ = 'Vendors'
    vendor_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    vendor_name = Column(String(100))
    brand_name = Column(String(100), unique=True)
    email = Column(String(100), unique=True)
    contact = Column(String(10), unique=True)
    created_at = Column(DATETIME, nullable=False)

    shop_addresses = relationship('VendorAddress', back_populates='vendor', cascade='all, delete-orphan')
    products = relationship('Product', back_populates='vendor', cascade='all, delete-orphan')
